"""Engine unit tests: pure logic only (no network, no ffmpeg), so they run anywhere in seconds."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from faceless import analytics, config, moneymath
from faceless.gauntlet import check_package, check_script, score
from faceless.pipeline.captions import callout_text, chunk_words, wrap_hook
from faceless.pipeline.ideate import similarity
from faceless.pipeline.script import normalize, word_count
from faceless.pipeline.voice import align_beats, attach_display
from faceless.providers.tts import rate_to_speed, speed_to_rate
from faceless.state import Job, TransitionError

SEED = Path(__file__).resolve().parent.parent / "script-lab" / "final" / "_seed-001-ronald-read.json"


def words(*tokens, step=0.3):
    return [{"w": t, "start": round(i * step, 3), "end": round(i * step + step * 0.9, 3)} for i, t in enumerate(tokens)]


# ---- money math -------------------------------------------------------------------------------

def test_future_value_matches_known_value():
    assert round(moneymath.future_value_monthly(200, 0.08, 40)) == 698202


def test_card_payoff_with_fixed_payment():
    months, interest = moneymath.card_payoff(3000, 0.24, 300)
    assert months == 12 and 370 < interest < 400


def test_card_payoff_never_ends_when_payment_below_interest():
    months, interest = moneymath.card_payoff(10000, 0.24, 100)
    assert interest == float("inf")


def test_fact_sheet_mentions_assumptions():
    sheet = moneymath.fact_sheet()
    assert "8%/yr" in sheet and "24% APR" in sheet


# ---- voice alignment ---------------------------------------------------------------------------

def test_attach_display_restores_punctuation():
    w = attach_display(words("Not", "his", "friends", "Not", "his", "neighbors"), "Not his friends. Not his neighbors.")
    assert [x["display"] for x in w] == ["Not", "his", "friends.", "Not", "his", "neighbors."]


def test_attach_display_merges_split_tokens():
    w = attach_display(words("J", "C", "Penney", "for"), "J.C. Penney for")
    assert [x["display"] for x in w] == ["J.C.", "Penney", "for"]
    assert w[0]["end"] == pytest.approx(0.57)


def test_attach_display_keeps_raw_words_when_streams_disagree():
    raw = words("eight", "million", "dollars")
    assert attach_display(raw, "$8M") == raw


def test_align_beats_starts_at_zero_and_is_contiguous():
    ws = words("One", "two", "three", "four", "five", "six")
    spans = align_beats(["One two three.", "Four five six."], ws, total=2.0)
    assert spans[0][0] == 0.0
    assert spans[0][1] == spans[1][0] == pytest.approx(0.9)
    assert spans[1][1] == 2.0


def test_rate_speed_roundtrip():
    assert rate_to_speed("+14%") == pytest.approx(1.14)
    assert speed_to_rate(0.94) == "-6%"


# ---- captions ----------------------------------------------------------------------------------

def test_chunks_break_at_sentence_end():
    ws = [{"w": t, "display": t, "start": 0, "end": 0} for t in "He pumped gas. Then he cleaned floors.".split()]
    chunks = [" ".join(x["display"] for x in c) for c in chunk_words(ws, 3, 16)]
    assert "gas." in chunks[0] and all("gas. Then" not in c for c in chunks)


def test_chunks_do_not_end_on_weak_word():
    ws = [{"w": t, "display": t, "start": 0, "end": 0} for t in "He bought a house in the city".split()]
    for c in chunk_words(ws, 3, 16)[:-1]:
        assert c[-1]["display"].lower() not in {"a", "the", "in"}


def test_hook_wraps_without_escaping_newlines():
    lines = wrap_hook("A janitor died with $8 million")
    assert len(lines) == 2 and all("\\" not in l for l in lines)


def test_long_callout_wraps_smaller():
    text, size = callout_text("25 years at a gas pump")
    assert "\\N" in text and size < 150
    assert callout_text("$698,000") == ("$698,000", 150)


# ---- scripts + gauntlet ------------------------------------------------------------------------

def seed_script():
    return normalize(json.loads(SEED.read_text(encoding="utf-8")))


def test_seed_script_passes_code_gates():
    gates = check_script(seed_script(), history=[])
    s, hard = score(gates)
    assert not hard, [g.name for g in hard]
    assert s >= 90


def test_compliance_gate_blocks_promises():
    scr = seed_script()
    scr["beats"][3]["say"] = "This fund has guaranteed returns, you should buy it now."
    hard = {g.name for g in check_script(scr, history=[]) if g.hard and not g.passed}
    assert "compliance_phrases" in hard


def test_originality_gate_blocks_duplicates():
    scr = seed_script()
    hard = {g.name for g in check_script(scr, history=[scr["title"] + " " + scr["beats"][0]["say"]])
            if g.hard and not g.passed}
    assert "originality" in hard


def test_judge_compliance_ignores_factual_score(monkeypatch):
    """Compliance risk 4 with stated assumptions passes; factual risk is judged by its own gate."""
    from faceless import gauntlet
    monkeypatch.setattr(gauntlet.llm, "complete", lambda *a, **k: {
        "hook": 8, "retention": 7, "value": 7, "factual_risk": 6, "compliance_risk": 4,
        "suspect_claims": ["x"], "fixes": []})
    monkeypatch.setattr("faceless.decide.RECORDS", Path("/dev/null"))
    monkeypatch.setattr("faceless.events.JOURNAL", Path("/dev/null"))
    gates = {g.name: g for g in gauntlet.judge_script(seed_script())[0]}
    assert gates["judge_compliance"].passed
    assert not gates["judge_facts"].passed


def test_word_count_hard_only_when_far_out_of_range():
    scr = seed_script()
    gate = lambda s: next(g for g in check_script(s, history=[]) if g.name == "word_count")  # noqa: E731
    near = dict(scr, beats=scr["beats"][:-1])            # a few words short: soft
    far = dict(scr, beats=scr["beats"][:8])              # ~60 words short: hard, rewrite in the script loop
    assert not gate(near).hard or gate(near).passed
    assert gate(far).hard and not gate(far).passed


def test_length_brief_gives_a_word_target():
    from faceless.orchestrator import length_brief
    brief = length_brief(53.3, 124)
    assert "too short" in brief and "about 187 words" in brief


def test_normalize_strips_hook_punctuation():
    assert normalize({"title": "t", "hook_text": "21 YEARS.", "beats": []})["hook_text"] == "21 YEARS"


def test_normalize_clears_callout_on_hook_beat():
    scr = normalize({"title": "t", "beats": [{"say": "a b", "callout": "X", "visual": "v"}]})
    assert scr["beats"][0]["callout"] == ""


def test_word_count():
    assert word_count({"beats": [{"say": "one two"}, {"say": "three"}]}) == 3


def test_package_gate_requires_disclaimers():
    bad = {"description": "great video", "caption": "#money"}
    good = {"description": "Educational content, not financial advice. Narration and visuals are AI-assisted.",
            "caption": "#money"}
    assert any(g.hard and not g.passed for g in check_package(bad))
    assert not any(g.hard and not g.passed for g in check_package(good))


def test_similarity_is_symmetric_and_bounded():
    a, b = "janitor died with 8 million", "the janitor who died with $8 million"
    assert 0 <= similarity(a, b) <= 1 and similarity(a, b) == similarity(b, a)


# ---- routing + state ---------------------------------------------------------------------------

def test_allocate_balanced_by_default():
    weights = {p.id: 1.0 for p in config.load()["pillars"]}
    plan = analytics.allocate(5, weights, day_index=3)
    assert sorted(plan) == sorted(weights)


def test_allocate_favours_winners_but_caps_at_two():
    weights = {"story": 3.0, "math": 1.0, "psychology": 0.4, "myth": 0.4, "playbook": 0.4}
    plan = analytics.allocate(5, weights, day_index=0)
    assert plan.count("story") == 2 and len(plan) == 5


def test_job_cannot_move_backwards(tmp_path, monkeypatch):
    monkeypatch.setattr("faceless.config.Paths.jobs", tmp_path)
    monkeypatch.setattr("faceless.events.JOURNAL", tmp_path / "journal.jsonl")
    job = Job(id="t", pillar="story", topic="x", day="2026-01-01")
    job.advance("scripted")
    job.advance("voiced")
    with pytest.raises(TransitionError):
        job.advance("scripted")
    assert job.reached("scripted") and not job.reached("rendered")
