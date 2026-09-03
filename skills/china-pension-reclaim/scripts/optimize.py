#!/usr/bin/env python3
"""
Adversarial optimization pass over the claim kit, run on Claude Fable 5.1 via OpenRouter.

Four reviewers with different incentives read the artifact in parallel, then a synthesis
pass deduplicates and ranks what they found. The point is blind spots: findings the author
of the page could not have surfaced by re-reading their own work.

    export OPENROUTER_API_KEY=sk-or-v1-...
    python3 optimize.py --target ../assets/reclaim-app.html --brief case.md --out findings.json

Notes on the model:
  * Fable 5.1 has thinking always on. Do NOT send temperature/top_p/top_k, and do NOT send
    a thinking budget - the Anthropic API rejects all of them. OpenRouter silently drops
    temperature rather than surfacing the 400, which hides the mistake; omit it anyway.
  * Depth is controlled with reasoning.effort, which OpenRouter maps to Anthropic's
    output_config.effort. "high" is the sweet spot; "max" roughly doubles spend.
  * Streaming, because a high-effort review on a 50KB artifact can run several minutes and
    a non-streamed request will hit the HTTP timeout first.
"""

import argparse, concurrent.futures, json, os, re, sys, time
import urllib.request, urllib.error

MODEL = "anthropic/claude-fable-5.1"
ENDPOINT = "https://openrouter.ai/api/v1/chat/completions"

REVIEWERS = {
    "domain": (
        "You are a Chinese social-insurance caseworker who has personally processed hundreds of "
        "foreign-national personal-account terminations at a district branch in Shanghai. You know "
        "what actually happens at the counter, as opposed to what the published service guide says. "
        "Find every place this page would send a claimant to the counter and get them turned away. "
        "Be specific about the regulation, the form, or the counter habit involved."
    ),
    "adversary": (
        "You are the claimant: broke, abroad, no Chinese, burned once already by an employer that "
        "vanished, and sceptical that this money exists at all. Read this page looking for the moment "
        "you would give up, the instruction you could not physically carry out from where you are, and "
        "anything that reads like it was written by someone who has never had to do this. Also flag "
        "anything that would make you distrust the page."
    ),
    "risk": (
        "You are a compliance and consumer-protection reviewer. Identify where this page could cause "
        "real harm: financial advice that is wrong for a subset of readers, irreversible actions "
        "presented too casually, tax consequences, immigration consequences, scam exposure, privacy "
        "exposure, statute-of-limitation traps, and any claim stated with more confidence than the "
        "underlying rule supports."
    ),
    "product": (
        "You are a product lead who ships tools that recover money for people. Ignore polish. Identify "
        "what is MISSING: the feature whose absence caps how much money this recovers or how many "
        "people it reaches. Rank by expected value recovered per unit of build effort. Be concrete "
        "enough that an engineer could start on it today."
    ),
}

SCHEMA_INSTRUCTION = """
Return ONLY a JSON object, no prose around it, no markdown fence:

{"findings":[{
  "title": "short imperative, max 12 words",
  "severity": "critical|high|medium|low",
  "category": "correctness|missing-feature|harm|usability|trust",
  "blind_spot": true or false,
  "detail": "2-4 sentences: what is wrong or missing, and why it matters",
  "fix": "the concrete change to make, specific enough to implement",
  "money_at_stake": "rough RMB or ZAR impact, or 'none' if not financial"
}]}

Rules:
- Set blind_spot true only when the author could NOT have found this by re-reading their own
  page - it requires outside knowledge or a perspective they do not have.
- Do not pad. Six sharp findings beat twenty soft ones.
- Do not restate what the page already does well.
"""


def call(messages, effort="high", max_tokens=16000, retries=3):
    """One streamed chat completion. Returns the assembled text."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        sys.exit("OPENROUTER_API_KEY is not set")

    body = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "stream": True,
        "reasoning": {"effort": effort},
        # deliberately no temperature / top_p / top_k - Fable rejects them upstream
    }
    req_headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "X-Title": "china-pension-reclaim-optimizer",
    }

    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                ENDPOINT, data=json.dumps(body).encode(), headers=req_headers, method="POST"
            )
            out = []
            with urllib.request.urlopen(req, timeout=1800) as resp:
                for raw in resp:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line.startswith("data: "):
                        continue
                    payload = line[6:]
                    if payload == "[DONE]":
                        break
                    try:
                        chunk = json.loads(payload)
                    except json.JSONDecodeError:
                        continue
                    for ch in chunk.get("choices", []):
                        piece = (ch.get("delta") or {}).get("content")
                        if piece:
                            out.append(piece)
            text = "".join(out).strip()
            if text:
                return text
            last = "empty response"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read().decode('utf-8','replace')[:400]}"
            if e.code in (400, 401, 403):
                break  # not retryable
        except Exception as e:  # noqa: BLE001 - network layer, any failure is retryable
            last = f"{type(e).__name__}: {e}"
        time.sleep(2 ** attempt)
    raise RuntimeError(f"call failed after {retries} attempts: {last}")


def parse_json(text):
    """Fable returns clean JSON, but fence it defensively anyway."""
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", text, re.S)
        if m:
            return json.loads(m.group(0))
        raise


def review(name, persona, artifact, brief, effort):
    prompt = (
        f"{persona}\n\n"
        f"## The case this tool was built around\n{brief}\n\n"
        f"## The artifact, in full\n```html\n{artifact}\n```\n\n"
        f"{SCHEMA_INSTRUCTION}"
    )
    t0 = time.time()
    raw = call([{"role": "user", "content": prompt}], effort=effort)
    data = parse_json(raw)
    for f in data.get("findings", []):
        f["reviewer"] = name
    print(f"  [{name}] {len(data.get('findings', []))} findings in {time.time()-t0:.0f}s", file=sys.stderr)
    return data.get("findings", [])


def synthesize(findings, brief, effort):
    prompt = (
        "You are the engineering lead deciding what actually gets built this week. Below are findings "
        "from four independent reviewers of the same tool. They overlap and some are wrong.\n\n"
        f"## The case\n{brief}\n\n"
        f"## Raw findings\n{json.dumps(findings, indent=2, ensure_ascii=False)}\n\n"
        "Merge duplicates, discard anything that is speculation rather than a real defect, and return "
        "the surviving findings ranked by (money recovered or harm avoided) divided by implementation "
        "effort. Keep the same JSON schema, and add to each finding an integer \"rank\" starting at 1 "
        "and a \"verdict\" of \"build\" or \"note\" - \"build\" means it changes the artifact, \"note\" "
        "means it belongs in the written guidance instead.\n\n" + SCHEMA_INSTRUCTION
    )
    raw = call([{"role": "user", "content": prompt}], effort=effort, max_tokens=20000)
    return parse_json(raw).get("findings", [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True, help="artifact file to review")
    ap.add_argument("--brief", required=True, help="markdown file describing the case")
    ap.add_argument("--out", default="findings.json")
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high", "xhigh", "max"])
    ap.add_argument("--reviewers", default="all")
    args = ap.parse_args()

    artifact = open(args.target, encoding="utf-8").read()
    brief = open(args.brief, encoding="utf-8").read()

    picked = REVIEWERS if args.reviewers == "all" else {
        k: v for k, v in REVIEWERS.items() if k in args.reviewers.split(",")
    }
    print(f"Reviewing {args.target} ({len(artifact):,} chars) "
          f"with {len(picked)} reviewers on {MODEL} at effort={args.effort}", file=sys.stderr)

    raw_findings = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(picked)) as pool:
        futures = {
            pool.submit(review, n, p, artifact, brief, args.effort): n for n, p in picked.items()
        }
        for fut in concurrent.futures.as_completed(futures):
            try:
                raw_findings.extend(fut.result())
            except Exception as e:  # noqa: BLE001 - one reviewer failing must not sink the run
                print(f"  [{futures[fut]}] FAILED: {e}", file=sys.stderr)

    if not raw_findings:
        sys.exit("no findings returned - check the API key and model access")

    print(f"Synthesizing {len(raw_findings)} raw findings...", file=sys.stderr)
    final = synthesize(raw_findings, brief, args.effort)
    final.sort(key=lambda f: f.get("rank", 999))

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump({"model": MODEL, "effort": args.effort, "target": args.target,
                   "raw_count": len(raw_findings), "findings": final}, fh,
                  indent=2, ensure_ascii=False)

    print(f"\n{len(final)} findings -> {args.out}\n", file=sys.stderr)
    for f in final:
        flag = " [BLIND SPOT]" if f.get("blind_spot") else ""
        print(f"{f.get('rank','?'):>2}. [{f.get('severity','?'):<8}] {f.get('verdict','?'):<5} "
              f"{f.get('title','?')}{flag}")


if __name__ == "__main__":
    main()
