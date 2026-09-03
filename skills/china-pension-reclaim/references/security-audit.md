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
