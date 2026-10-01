# Quiet Money Studio: a faceless video engine

Five 61-72 second vertical videos a day about money psychology and personal finance: researched script,
neural voiceover, cinematic AI stills with motion, word-by-word captions, original music, quality-gated,
packaged, and scheduled. Runs daily on GitHub Actions for under $1/day.

```
idea backlog → script (Gemini) → judge + gates → voice (Edge TTS) → images (FLUX.2) → render (FFmpeg)
            → gauntlet (30+ gates) → posting pack → Upload-Post (TikTok / Shorts / Reels) → metrics → pillar weights
```

## Quick start (local)

```bash
cd faceless-studio
pip install -r requirements.txt          # + ffmpeg on PATH
export GEMINI_API_KEY=... CLOUDFLARE_API_KEY=... CLOUDFLARE_ACCOUNT_ID=...
python -m faceless doctor
python -m faceless make --pillar story    # one video
python -m faceless daily                  # the full day
```
Output: `distribution/queue/<day>/slot<N>-<pillar>/` with `video.mp4`, `cover.jpg`, `POST.md`.

## Run it without you (GitHub Actions)

`.github/workflows/faceless-daily.yml` runs every day at 09:17 UTC (and on demand from the Actions tab):
produces the batch, schedules posts, uploads the packs as a downloadable artifact, and commits state and reports.

Add these repository secrets (Settings → Secrets and variables → Actions):

| Secret | Required | Where to get it |
|---|---|---|
| `GEMINI_API_KEY` | yes | aistudio.google.com → API keys (free tier) |
| `CLOUDFLARE_API_KEY`, `CLOUDFLARE_ACCOUNT_ID` | yes | Cloudflare dashboard → API Tokens (Workers AI: Read/Edit) |
| `OPENROUTER_API_KEY` | recommended | openrouter.ai → keys (paid fallbacks, cents) |
| `UPLOAD_POST_API_KEY`, `UPLOAD_POST_USER` | for auto-posting | upload-post.com → API key + profile name with TikTok/YouTube/IG connected |
| `ELEVENLABS_API_KEY` | optional | premium voice |
| `TYPESAFE_API_KEY` | optional | Jev decision layer (starts in dry-run) |
| `COMPOSIO_API_KEY` | recommended | dashboard.composio.dev → Platform → project key (`ak_...`): YouTube/TikTok/Drive connections, see `.claude/skills/faceless-composio` |

Without Upload-Post secrets the workflow still builds every pack: download the artifact and post from your phone.

## What only you can do (one time)
1. Create the TikTok, YouTube, and Instagram accounts with one handle; set `[channel].handle` in `studio.toml`.
2. Make a free link-in-bio page with the lead magnet + affiliate links; set `[channel].link_in_bio`.
3. Apply to 2-3 finance affiliate programs available in your country (see `channel/monetization.md`).
4. Connect the accounts in Upload-Post and add the secrets above.
5. Once a week: paste performance numbers (or connect analytics) so the engine learns (`analytics/CONTEXT.md`).

## Map
| Folder | Role |
|---|---|
| `CLAUDE.md` | Studio identity + routing table (start here) |
| `studio.toml` | All settings: brand, pillars, providers, budgets, schedule |
| `channel/` | Brand bible, monetization, compliance |
| `script-lab/` | Topic backlog, drafts, final scripts |
| `production/` | Render pipeline docs; output (gitignored) |
| `distribution/` | Posting packs and platform rules |
| `analytics/` | Metrics in, pillar weights out |
| `gauntlet/` | Quality gates, reports, the improvement log |
| `repo-farm/` | Which external repos/tools are active, parked, or rejected |
| `faceless/` | The engine (Python) + `CONTEXT.md` architecture |
| `state/` | Journal, jobs, ledger, decision records |
| `tests/` | `python -m pytest -q tests` |

Skills for Claude Code live in `/.claude/skills/faceless-*` (daily, script, gauntlet, trends, publish, analytics).
