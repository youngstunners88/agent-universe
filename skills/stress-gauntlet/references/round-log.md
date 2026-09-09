# Round log — china-pension-reclaim

What each round found, what was fixed, and what was ruled not-applicable. Kept so the next run
starts informed instead of rediscovering the same ground.

## Pre-gauntlet rounds (ad hoc, before this skill existed)

**Security pass.** Ran a generic pre-deploy checklist built for backend SaaS against a static
single-file app. Six "blockers" — rate limiting, Sentry, ToS/privacy policy, data export/delete,
lockfile, asset licensing — all false positives for a page with no server, no dependencies and no
data collection. The one real finding came from tracing by hand, not from the scanner: `speak()`
passed the passport number to the Web Speech API, and non-local voices are cloud TTS on most
platforms, so pressing play could send it to a third party — contradicting the page's own
"nothing leaves your browser" line. Fixed by requiring `localService === true`.

**Correctness gauntlet.** Eleven fixes. The two that mattered: a returning visitor with stale
`localStorage` from before the district field became a `<select>` hit a hard `TypeError` on every
load (`options[-1].text`) with no recovery but clearing site data; and `mi()` trusted
`split("-")` on a `type="month"` field, which Firefox desktop renders as free text — malformed
input became `NaN`, and since `NaN` compares false against everything, every guard meant to catch
bad data failed open and "¥NaN" reached the screen. Also fixed: a self-inflicted bug where the
previous round's own fix produced a phantom contributing month whenever `from === s`.

**Recurring lesson.** A fallback that *usually* computes the right answer through incidental
arithmetic is not a fix. Handle the unknown case explicitly and return early.

## Round 1 — multi-city + pasted-record parser

Scope: per-city base tables and enrolment dates (Beijing priced from its own published table),
and a parser that turns a pasted 参保缴费明细 into per-month declared bases.

Found before the agents even ran, during the feature's own first test: the month regex
alternated `(0?[1-9]|1[0-2])`, so `2021-10` matched the leading `1` and became `2021-01` —
collapsing Oct/Nov/Dec into a duplicate January and inventing ten missing months. Alternation
order in a regex is not cosmetic; two-digit alternatives must come first, plus `(?!\d)`.

*(Agent findings appended below as rounds complete.)*
