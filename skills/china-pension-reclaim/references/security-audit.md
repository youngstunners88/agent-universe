# Security audit — reclaim-app.html

Run against Kofi's `secure-build-checklist` skill (a general pre-deploy gate for services with a
backend). Recorded here so the routine is repeatable, not one-off.

## Why most of the checklist doesn't apply

The tool is a single static HTML file with no server, no database, no npm dependencies, and no
build step. It ran clean at `--fail-on=low` except for six findings, all false positives for this
project shape:

| Check | Why it's not applicable here |
|---|---|
| API001 rate limiting | No server endpoints exist to rate-limit. |
| LOG001 error tracking (Sentry etc.) | No production server to instrument. |
| DATA001 Terms of Service / Privacy Policy | No data is collected or transmitted — see below. |
| DATA002 export/delete flow | Already exists: the "Clear my details" button wipes `localStorage`. |
| DEP002 lockfile committed | No package manager — zero dependencies, nothing to lock. |
| DATA003 asset licensing | Only external asset is Google Fonts (SIL OFL, embedded via `<link>`, not shipped). |

**Do not treat an automated scanner's pass/fail as the audit.** Its "Injection & Input
Validation" category passed cleanly, but its checks are regex-based and this project's real risk
— free-text fields flowing into `innerHTML` — needed a manual trace to actually verify.

## What the manual trace found

Every free-text field (`f-name`, `f-pp`, `f-ppold`, `f-agn`, `f-agid`, `f-agph`) was walked to
every place it's read, across `cover-fields`, the call-script builder, and the generated
documents. Two sinks exist for user text: `.textContent` (auto-escaping, used for the power of
attorney and statement panes) and `innerHTML` after the local `esc()` helper (used for the
call-script lines and the cover strip). No field reaches `innerHTML` unescaped. `f-branch` is a
`<select>`, not free text, so it can't carry arbitrary input at all.

An `esc()`-before-`innerHTML` invariant comment is now in the source itself, directly above
`esc()`, so a future edit that adds a new field to a template without escaping it fails a code
read, not just a scan.

## The one real finding: speech synthesis could leak the passport number

`speak()` called the Web Speech API with the passport number embedded in the utterance text.
**On many systems the browser's non-local voices are cloud TTS** — Chrome's default voices
commonly synthesize server-side — so pressing the Mandarin playback button could have sent a
passport number to a third-party server, directly contradicting the page's own "nothing ever
leaves your browser" line in the footer.

Fixed: `speak()` now scans `speechSynthesis.getVoices()` for one with `localService === true` and
a `zh` language tag, and speaks only through that. If none exists on the device, the button says
"No offline voice" instead of silently falling back to a network one. A note next to the call
script explains why, so the behavior isn't a silent degrade.

## Also hardened

- `maxlength` added to every free-text input (80 for name, 20 for passport numbers and agent
  phone, 60 for agent name, 18 for a PRC ID number) — cheap defense in depth, and it's also just
  correct UX for fields with a known real-world maximum length.
- Confirmed zero network calls anywhere in the file (`fetch`, `XMLHttpRequest`, `sendBeacon`,
  `WebSocket` all absent) other than the two Google Fonts `<link>` tags.
- Confirmed no `eval`, `new Function`, or `document.write`.
- Confirmed no API keys or secrets are embedded (this app was built using research from several
  paid APIs during development; none of those credentials ever touch the shipped file).
- Confirmed the agent's PRC ID number (`f-agid`) — a third party's sensitive identifier, not just
  the user's own data — is included in the `SENSITIVE` gate that keeps it out of `localStorage`
  unless the user explicitly opts in via "Remember my passport and agent details."

## Re-running this

```bash
bun secure-build-checklist/scripts/audit.ts skills/china-pension-reclaim --fail-on=low --verbose
```

Expect the same six backend-shaped false positives every time; triage anything new against
whether this project actually has the surface the check assumes (a server, a dependency tree, a
data-collection flow) before treating it as real. Re-run after any change that adds a new
`innerHTML` template, a new form field, or any browser API that could touch the network.

## Gauntlet round 2 — bugs, not just injection

The first audit above focused on injection and data exposure. This round ran a broader gauntlet
— `/code-review` at high effort, `/security-review`, and two ad hoc Fable 5.1 personas (a browser
security engineer; a QA engineer trying to break the calculator with edge-case input) — against
correctness, not just security. Every finding was verified against the real code before fixing,
and every fix was tested with a concrete reproduction rendered through headless Chromium, not a
syntax check.

**The one that actually mattered:** a returning user with a stale `localStorage` entry from
before the district field's free-text-to-`<select>` conversion hit a real crash — `load()`
assigned the old value straight to the `<select>`, `selectedIndex` became `-1`, and `read()`
indexed `options[-1].text`, throwing on every page load with no recovery short of clearing site
data by hand. `load()` now verifies a stored `<select>` value against the element's own options
before assigning it — the general lesson: any code that replays persisted state into a `<select>`
needs this check, permanently, not just for the field that broke this time.

**Second:** Firefox desktop renders `type="month"` as plain text, so `mi()` trusted `split("-")`
on whatever the user typed. Malformed input became `NaN`, and `NaN` comparisons all evaluate
`false` — meaning every guard meant to catch bad data silently didn't. `mi()` now validates the
shape and returns `null` (same as "no date") otherwise.

**Third, a self-inflicted one:** the previous round's own fix for the blank-exit-date bug had its
own bug — a fallback value that happened to compute to zero in some cases and a phantom nonzero
month in others (specifically whenever `from === s`), plus a fabricated warning that contradicted
the correct one next to it. Root cause: trying to coerce an *unknown* value through the same
arithmetic as a real one, instead of returning early for the unknown case. This is the recurring
failure mode worth remembering — a fallback that "usually" produces the right answer through
incidental arithmetic is not the same as handling the case explicitly, and it will eventually be
wrong in some branch you didn't trace by hand.

Also fixed: unclamped percentage/salary/exchange-rate inputs (negative and absurd values flowed
straight through), a silent floor-price with no salary entered, no upper bound on the
contributing-month loop (a mistyped year could spin it into the millions), a user-typed salary
value reaching an HTML attribute without `esc()` (inconsistent with the file's own invariant, even
though `type="number"` makes it low-risk in practice), a floating-point display artifact
(`0.1 + 0.2` → `0.30000000000000004%`), the applicant's own name missing from the same persistence
gate as the agent's name, and a dead `required` attribute on an input the page never validates
(no `<form>`, nothing calls `checkValidity()`) that could mislead a future maintainer into
thinking the browser was enforcing something it wasn't.

### Running the gauntlet again

1. `bun secure-build-checklist/scripts/audit.ts skills/china-pension-reclaim --fail-on=low` —
   triage findings against whether the project actually has the surface the check assumes.
2. `/code-review high skills/china-pension-reclaim` and `/security-review` against the current
   diff.
3. A targeted adversarial pass with personas suited to what changed — a generic "review this"
   prompt does not reliably surface the kind of bug a fresh, adversarial read catches; distinct,
   conflicting personas do.
4. Fix, verify every fix with a concrete reproduction (a crafted input, a forged localStorage
   entry) rendered through headless Chromium — not just `node --check`.
5. Re-run step 2 against the fix itself before calling it done. This round's clean self-inflicted
   bug (the blank-exit fallback) was only caught because of this step — the first-pass fix looked
   correct and passed its own tests; only a second, independent read caught the edge case.
