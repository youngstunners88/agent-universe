---
name: stress-gauntlet
description: Run a multi-round adversarial stress test against a client-side web app to clear bugs and vulnerabilities before shipping. Fans out three specialised subagents (input fuzzing, client-side security, independent calculation verification) per round, fixes what they find, and re-runs until a round comes back clean. Use before publishing a tool people will act on, after adding features, or when asked to stress test, harden, or bulletproof an app.
---

# Stress Gauntlet

A convergence loop, not a single audit. Each round runs three specialists in parallel against
the *current* state of the app, you fix what they find, and the next round tests the fixes.
The loop ends when a round returns nothing real — not after a fixed number of rounds.

## Why three agents and not one

A single "review this" prompt returns generic findings. Three agents with narrow, conflicting
mandates return specific ones, and their blind spots don't overlap:

| Agent | Hunts | Would never find |
|---|---|---|
| `input-fuzzer` | Wrong numbers, NaN, crashes from hostile input | An XSS sink with safe-looking inputs |
| `webapp-security-auditor` | XSS, exfiltration, storage leaks, broken privacy claims | A rounding error |
| `calc-verifier` | Arithmetic that disagrees with an independent re-derivation | Anything not numeric |

## Running a round

Launch all three **in parallel in one message** — they don't depend on each other, and serial
runs triple the wall clock:

```
Agent(subagent_type="input-fuzzer", prompt="<app path> + what changed this round")
Agent(subagent_type="webapp-security-auditor", prompt="<app path> + what changed")
Agent(subagent_type="calc-verifier", prompt="<app path> + the rules it should implement")
```

Give each the file path, what changed since the last round, and any finding from a previous
round you believe is fixed — so they can confirm or refute it rather than rediscover it.

## Triaging what comes back

Verify every finding against the real code before fixing it. Agents are good but not
authoritative, and a confidently-wrong "fix" applied without checking is how you ship a
regression. For each finding decide: **real** (fix it), **already handled** (say where), or
**not applicable** (say why — this reasoning belongs in the write-up).

Bias toward fixing the root cause rather than the symptom. A fallback value that *usually*
computes the right answer through incidental arithmetic is not a fix; handle the case
explicitly.

## Verifying a fix

`node --check` proves syntax, nothing more. Every fix needs a **concrete reproduction** run
through headless Chromium — the literal input that used to break it, showing the new output:

```bash
# patch a specific value into a copy, render, and read the real output
python3 -c "s=open('app.html').read(); s=s.replace('value=\"2022-08\"','value=\"\"'); \
  open('/tmp/t.html','w').write(s)"
/opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --disable-gpu --no-sandbox \
  --dump-dom --virtual-time-budget=8000 "file:///tmp/t.html" 2>/dev/null | grep -o 'id="total">[^<]*'
```

Two traps worth knowing:
- `--dump-dom` serializes `<script>` source too, so grepping for a message string can match the
  code that *would* print it rather than rendered output. Check inside the target element.
- Setting `el.value` via JS does **not** update the reflected `value="..."` HTML attribute, so
  static inputs look unchanged in `--dump-dom`. Verify through computed output instead.

Finish each round by confirming the baseline still produces its original figures — a fix that
silently changes the normal-path result is a regression, however correct it looks.

## Ending the loop

Stop when a round produces no real findings. Record what each round found, what was fixed, and
which findings were ruled not-applicable and why, so the next run starts informed rather than
rediscovering the same ground. `references/round-log.md` is that record.
