"""Script stage: hand-written final scripts win; otherwise the LLM drafts from the five-part prompt."""

from __future__ import annotations

import json
import re

from faceless import config, events
from faceless.config import Paths
from faceless.prompts import script_prompt
from faceless.providers import llm


def narration(script: dict) -> str:
    return " ".join(b["say"].strip() for b in script["beats"])


def word_count(script: dict) -> int:
    return len(narration(script).split())


def normalize(script: dict) -> dict:
    beats = []
    for b in script.get("beats", []):
        say = re.sub(r"\s+", " ", str(b.get("say", ""))).strip()
        if not say:
            continue
        beats.append({"say": say, "callout": str(b.get("callout") or "").strip()[:28],
                      "visual": str(b.get("visual", "")).strip()})
    if beats:
        beats[0]["callout"] = ""  # the hook headline owns the top of the frame in beat 1
    tags = script.get("hashtags") or re.findall(r"#\w+", script.get("caption", ""))
    tags = [t if t.startswith("#") else f"#{t}" for t in tags][:6]
    return {
        "title": str(script.get("title", "")).strip()[:90],
        "hook_text": str(script.get("hook_text", "")).strip().rstrip(".!,;:"),
        "beats": beats,
        "caption": str(script.get("caption", "")).strip(),
        "description": str(script.get("description", "")).strip(),
        "hashtags": tags,
        "first_comment": str(script.get("first_comment", "")).strip(),
        "facts": script.get("facts", []),
        "source": script.get("source", "llm"),
        "pillar": script.get("pillar", ""),
    }


def final_path(job) -> object:
    return Paths.final / f"{job.id}.json"


def recent_titles(limit: int = 25) -> list[str]:
    titles = []
    for p in sorted(Paths.final.glob("*.json"))[-limit:]:
        try:
            titles.append(json.loads(p.read_text(encoding="utf-8")).get("title", ""))
        except json.JSONDecodeError:
            continue
    return [t for t in titles if t]


def write(job, angle: str = "", feedback: list[str] | None = None) -> dict:
    """Return the job's script, drafting one if no final script exists yet."""
    fp = final_path(job)
    if fp.exists() and not feedback:
        script = normalize({"pillar": job.pillar, **json.loads(fp.read_text(encoding="utf-8"))})
        events.emit("SCRIPT_LOADED", job=job.id, source=script["source"])
        return script
    pillar = config.pillar(job.pillar)
    prompt = script_prompt(pillar, job.topic, angle, feedback, recent_titles())
    from faceless.prompts import identity
    raw = llm.complete(prompt, system=identity(), want_json=True, job=job.id)
    raw["pillar"] = job.pillar
    script = normalize(raw)
    rnd = len(list(Paths.drafts.glob(f"{job.id}*.json")))
    (Paths.drafts / f"{job.id}.r{rnd}.json").write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")
    events.emit("SCRIPT_DRAFTED", job=job.id, words=word_count(script), beats=len(script["beats"]), round=rnd)
    return script


def finalize(job, script: dict) -> None:
    final_path(job).write_text(json.dumps(script, indent=2, ensure_ascii=False), encoding="utf-8")
