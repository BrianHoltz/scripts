---
name: ailert
description: >-
  Get the user's attention with a macOS alert dialog, escalating sounds, and
  text-to-speech. Use when an agent needs the user to act — login prompts,
  task completion, review requests, or any blocking wait. macOS only; no
  extra installs required.
allowed-tools:
  - Bash
metadata:
  author: Brian Holtz
  platform: macOS
  tags: notification, alert, attention, macos, sound, tts
sample-prompts:
  - "Alert the user that the build finished"
  - "Ask the user to log in to Grafana"
  - "Notify them the PR is ready for review"
  - "/ailert 15 Please check the deploy"
  - "/ailert -joke Your tests passed"
arguments:
  - <message> - optional, the alert message (default "Wibey needs your attention")
  - <timeout> - optional integer, seconds before speech escalation (default 30)
  - --joke - force the easter egg joke suffix (normally 25% random chance)
---

> [!NOTE]
> **Mirror-safe skill.** This file contains no Walmart-proprietary content and is
> designed to be manually mirrored to personal laptops. The canonical copy lives in
> [`relationship-shared/.wibey/skills/ailert/`](https://gecgithub01.walmart.com/CatalogRelationships/relationship-shared).
> **If you are reading this outside of Walmart GHE, do not edit it here** — make
> changes in relationship-shared and re-sync.

# ailert — macOS Alert + Escalating Sound + Speech

Get the user's attention when an agent is blocked waiting for human action.
Uses only built-in macOS tools (`osascript`, `afplay`, `say`) — zero dependencies.

## When to use

- Agent needs the user to **log in** (SSO, PingFed, Microsoft)
- A **long-running task completed** and the user may have walked away
- Agent needs a **decision or review** before proceeding
- Any situation where the user may not be watching the terminal

Other skills can invoke ailert programmatically — see § Calling from other skills.

## Argument parsing

Parse the `args` string for:

- **`--joke`** flag: if present, remove it from args and force joke mode
- **Timeout**: if the first remaining token is an integer, use it as timeout (seconds)
- **Message**: everything else is the message

Defaults: timeout = 30, message = "Wibey needs your attention"

## Easter egg (25% chance, or always with `--joke`)

Roll `$((RANDOM % 4))`; if 0 (or if `--joke`), append a joke to the message:

- **Request** (contains "please", "log in", "check", "help", "review", or is a question): append " …so I can take over the world"
- **Declaration** (everything else): append " Totally not a sign that I'm trying to take over the world."

Use the modified message for both alert and speech.

## Sound assets

Bundled in the skill's `assets/` directory:

| File | Description |
|---|---|
| `trek_communicator.mp3` | Star Trek TOS communicator chirp (2s) |
| `cylon_attention.wav` | BSG 1978 Cylon "Attention" (volume-reduced to 25%) |

## Execution

Resolve the assets path relative to this skill, then run as a single bash block:

```bash
# Resolve assets — works whether skill is in shared/ or ~/.wibey/
SKILL_DIR="$(dirname "$(readlink -f "$0" 2>/dev/null || echo "$0")")"
# When invoked by Wibey, use the known skill location:
for D in "$HOME/.wibey/skills/ailert/assets" \
         "$HOME/bin/.wibey/skills/ailert/assets" \
         "$HOME/src/relationship-shared/.wibey/skills/ailert/assets"; do
  [ -d "$D" ] && ASSETS="$D" && break
done
TIMEOUT=<TIMEOUT>
MSG="<MESSAGE>"
DELAY_1=$((TIMEOUT / 3))
DELAY_2=$((TIMEOUT * 2 / 3))

# Dialog with very long osascript timeout — we dismiss it after speech
osascript -e "display alert \"🌀 Wibey\" message \"$MSG\" giving up after 300" &
DIALOG_PID=$!

# Escalating sounds at 1/3 and 2/3 of timeout
( sleep "$DELAY_1" && afplay "$ASSETS/trek_communicator.mp3" ) &
SND1_PID=$!
( sleep "$DELAY_2" && afplay "$ASSETS/cylon_attention.wav" ) &
SND2_PID=$!

# Poll: wait for TIMEOUT or early user dismiss
ELAPSED=0
while [ $ELAPSED -lt $TIMEOUT ] && kill -0 $DIALOG_PID 2>/dev/null; do
  sleep 1
  ELAPSED=$((ELAPSED + 1))
done

if kill -0 $DIALOG_PID 2>/dev/null; then
  # Timed out — speak while dialog stays visible, then dismiss
  say "$MSG"
  kill $DIALOG_PID 2>/dev/null
else
  # User dismissed early — kill pending sounds
  kill $SND1_PID $SND2_PID 2>/dev/null
fi
wait $DIALOG_PID $SND1_PID $SND2_PID 2>/dev/null
```

### Behavior summary

| User action | What happens |
|---|---|
| Ignores alert | Communicator chirp at 1/3, Cylon "Attention" at 2/3, speech at timeout, then dialog closes |
| Clicks OK early | All pending sounds killed immediately, no speech |

## Calling from other skills

Other skills (e.g. grafana-read) or commands (e.g. safe-browse) can invoke ailert by running:

```
/ailert 30 Please log in to Walmart SSO so Wibey can access Grafana
```

Or by directly executing the bash pattern above with the assets path.

## Requirements

- **macOS** (uses `osascript`, `afplay`, `say` — all ship with macOS)
- No Homebrew packages, no npm, no extra installs
