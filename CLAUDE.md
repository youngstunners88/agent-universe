# Agent Universe

**Canonical home of the studio: https://github.com/youngstunners88/quiet-money (public).** Develop there;
this copy is the incubation history.

This repo holds two things:

1. **`faceless-studio/`**: the live business. An autonomous faceless short-video channel
   ("Quiet Money", money psychology and personal finance) that produces 5 videos a day.
2. **`skills/` + `SKILL.md` + `assets/`**: the original agent-universe blueprints
   (agent builders, orchestrators, voice agent). Reference material; not wired into the studio.

## Routing

| Task | Go to | Read first |
|---|---|---|
| Anything about the channel, videos, scripts, posting, money | `faceless-studio/` | `faceless-studio/CLAUDE.md` |
| Run today's videos / fix a failed run | `faceless-studio/` | `.claude/skills/faceless-daily/SKILL.md` |
| Agent-universe architecture, agent templates | `skills/`, `assets/` | `SKILL.md` |
| Evaluate an external repo/tool | `faceless-studio/repo-farm/` | `repo-farm/CONTEXT.md` |

## Rules
- Secrets live in environment variables / GitHub Actions secrets. Never write a key into a file.
- Run engine commands from `faceless-studio/`: `python -m faceless <command>`.
- Rendered media (`production/output`, `distribution/queue/**/*.mp4`) is gitignored; state and reports are committed.
