# Optimization workflow

`optimize.py` runs an adversarial review pass over the claim kit using **Claude Fable 5.1**
(`anthropic/claude-fable-5.1`) through OpenRouter.

The point is blind spots — findings the author of a page cannot reach by re-reading their own
work, because they require either outside domain knowledge or a perspective the author does not
hold. A single "review this" prompt does not produce them. Four reviewers with genuinely
conflicting incentives do.

## Running it

```bash
export OPENROUTER_API_KEY=sk-or-v1-...
python3 optimize.py --target ../assets/reclaim-app.html --brief case.md --effort high
```

| Flag | Default | Notes |
|---|---|---|
| `--target` | — | The artifact to review. Sent in full; the 1M context window makes chunking unnecessary. |
| `--brief` | — | Markdown describing the case and the facts the tool must get right. |
| `--effort` | `high` | `low` → `max`. `high` is the sweet spot; `max` roughly doubles spend for thoroughness that rarely changes the ranking. |
| `--reviewers` | `all` | Comma-separated subset, e.g. `domain,risk`. |
| `--out` | `findings.json` | Ranked findings with `verdict: build \| note`. |

Standard library only — no dependencies to install.

## The four reviewers

| Reviewer | Incentive | What it reliably catches |
|---|---|---|
| `domain` | A caseworker who has processed these at the counter | The gap between the published service guide and what actually happens at the window |
| `adversary` | The claimant: broke, abroad, no Chinese, already burned once | The exact step where a real person gives up |
| `risk` | Compliance and consumer protection | Irreversible actions presented too casually; confidence exceeding what the rule supports |
| `product` | Ships tools that recover money | What is *missing* — the absent feature that caps how much gets recovered |

A synthesis pass then merges duplicates, discards speculation, and ranks by value recovered per
unit of implementation effort.

## Cost and runtime

Roughly **$1.50 and 5 minutes** for a 50 KB artifact at `high` effort — four parallel reviews of
~200s each, then synthesis. Fable 5.1 is $10/$50 per MTok. The four reviewers run concurrently,
so wall-clock is one review plus the synthesis.

## Model notes that matter

Fable 5.1 is not shaped like an OpenAI-compatible chat model, and OpenRouter's compatibility
layer hides some of that:

- **Send no `temperature`, `top_p`, or `top_k`.** The Anthropic API rejects all three with a 400.
  OpenRouter silently drops them instead of surfacing the error, so the mistake is invisible —
  omit them anyway rather than relying on the router to clean up after you.
- **Thinking is always on.** Do not send a thinking budget; `budget_tokens` is rejected. Depth is
  controlled by `reasoning.effort`, which OpenRouter maps to Anthropic's `output_config.effort`.
- **Stream.** A high-effort review of a 50 KB artifact runs several minutes; a non-streamed
  request hits the HTTP timeout first.
- **Do not force tool choice.** `tool_choice: any|tool` returns a 400 on this model. This script
  asks for JSON in the prompt and parses defensively, which sidesteps it entirely.

## What came out of the first run

32 raw findings → 18 after synthesis, 12 flagged as genuine blind spots. The highest-value ones:

1. **The housing fund's employer share is also recoverable** — absent from the estimator
   entirely, and for the sample case worth more than the pension account.
2. **A credit to a Chinese bank account is not money in hand** — the kit ended at "paid out" and
   said nothing about getting it across a border.
3. **Departure date and employment-end date are different dates** — conflating them both
   overstated the balance and produced a sworn statement contradicting the passport stamp.
4. **The phone call was over-promised** — 12333 will not read account data to an unverified
   caller, and claimants read that refusal as "no account exists" and stop.

All fifteen `build` findings are implemented in the current kit.
