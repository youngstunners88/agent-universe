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

## Round 2 — security auditor + input fuzzer

**Security (1 high, 1 medium, 2 low).** "Clear my details" cleared name, passport and agent
fields but never the pasted contribution record — it stayed in the textarea, in memory and on
screen. A privacy control whose label overstates what it does is worse than none, because people
act on it. Also: the footer claimed everything stays in the browser without mentioning the Google
Fonts request (true of typed data, not of the visitor's IP); `esc()` escaped angle brackets but
not quotes while being used in an attribute context; and the JSON export didn't distinguish
figures derived from a real government record from modelled estimates.

Confirmed clean, worth recording so a later round doesn't re-litigate it: the parser's innerHTML
output is safe *by construction* — every interpolated value is either numeric or drawn from a
hardcoded status whitelist — and the share link cannot carry the record, which isn't in the
persisted-field map at all.

**Fuzzing (2 critical, 2 high, 4 medium).** Five ways the parser produced confidently wrong
numbers. The worst: a header row reading `月份(格式如2020-01)` claimed that month, and first-wins
dedup then discarded the *genuine* row — a real month replaced by ¥2,020. Also the year itself
winning as the base (2019 sits inside the plausible-amount range), an employee ID outranking the
real figure, `-3000.00` booked as a positive contribution, and a 38-month footer total booked as
one month.

## Round 3 — fuzzing the rewrite

New code is where new bugs live, and the round-2 rewrite had six of its own.

- `NOISE` matched substrings, so 合计 fired inside 综合计算 ("comprehensive calculation") and
  `total` inside `subtotal`, **dropping legitimate rows entirely**.
- The reversal check `/[-−(（]\s*\d/` scanned the whole line, so an ordinary Chinese document
  number `(2020)128号` or a hyphenated phone number disqualified a valid row.
- **Critical:** with two plausible figures on one line — a base beside a year-end bonus —
  `Math.max` silently booked the bonus. In band, so no out-of-range flag fired either.
- Duplicate months kept the *larger* base, so a genuine downward correction (更正为) lost to the
  overstated original.

Fixed by judging sign and labelling **per number rather than per line**, preferring a figure the
record itself labels 缴费基数, treating two unlabelled candidates as *ambiguous* rather than
guessing, anchoring the noise vocabulary, and letting later rows supersede earlier ones.

I also caught one of my own while briefing this round: round 2 preferred decimal figures
unconditionally, so `2019-03  12000  960.00` — base as a bare integer — lost both months as
unreadable.

**The lesson this project keeps re-teaching.** Every round, the worst bug was a rule that was
right about the case it was written for and silently wrong about a neighbouring one. And each
time the dangerous direction was the same: **silently dropping or mis-valuing real data beats
letting junk through**, because junk is visible in the table and a dropped month is not. A
preference rule needs a fallback; a heuristic that can't tell needs to say so rather than guess.

A 14-case regression suite covering all three rounds lives in the session scratchpad pattern
described in SKILL.md — extract `parseRecord` verbatim and run it under node.
