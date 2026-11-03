# Locate the commit that introduced this regression

A regression was reported against `NousResearch/hermes-agent`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Bug]: qqbot approval buttons rejected as unauthorized in named-profile sessions (session-key namespace vs "main")

### Summary

In a **named profile** (gateway multiplexing), every approval-button click (`allow-once` / `allow-always` / `deny`) in a QQ session is rejected as unauthorized:

```
[QQBot:...] Interaction: scene=c2c button_data='approve:agent:<profile>:qqbot:dm:<openid>:allow-once' operator=<openid>
[QQBot:...] Rejected unauthorized approval click for session agent:<profile>:qqbot:dm:<openid> (operator=<openid>)
```



### Root cause



```python
parts = str(session_key or "").split(":")
if len(parts) < 5 or parts[0] != "agent" or parts[1] != "main":
    return None
```

But `build_session_key()` namespaces named-profile keys as `agent:<profile>:...` (`gateway/session.py::_session_key_namespace()`), explicitly documented as position-compatible ("existing sessions and all positional parsers (`parts[2]` == platform, etc.) are unaffected"). For a named profile, `parts[1] == "<profile>" != "main"` → the parse returns `None` → `_is_authorized_interaction_for_session()` returns `False` → the click is dropped.

How the profile-namespaced key reaches the buttons:

1. `gateway/run.py` `_approval_notify_sync` — `_approval_session_key = ctx.session_key` (the real, profile-namespaced key)
2. passed to `send_exec_approval(session_key=...)`
3. `gateway/platforms/qqbot/keyboards.py::build_approval_keyboard` embeds it into `button_data` (`approve:<session_key>:<decision>`)
4. click → `INTERACTION_CREATE` → `_default_interaction_dispatch` → `_is_authorized_interaction_for_session` → rejected

### Reproduction

Deterministic, unit-level (no live QQ deployment needed):

```python
from gateway.platforms.qqbot.adapter import QQAdapter

QQAdapter._parse_gateway_session_key("agent:coder:qqbot:dm:u-1")
# → None   (expected: {"platform": "qqbot", "chat_type": "dm", "chat_id": "u-1"})
```

Live setup: run the gateway with a named multiplex profile serving QQBot, trigger a dangerous command in that profile's QQ chat, click an approval button → `Rejected unauthorized approval click` in the gateway log → approval times out BLOCKED.

### Why this is not the dm/c2c family

#32528 / #34432 / #40655 / #98100 are all about the **chat_type** slot (`dm` vs `c2c` in `_is_authorized_interaction_for_session`).   QQBot has none.

The namespace slot takes no part in any authorization decision — the `platform == "qqbot"`, `operator == chat_id` (c2c) and `operator == session_user` (group/guild) checks are what authorize — so accepting any non-empty namespace does not weaken the check.

### Suggested fix

In `_parse_gateway_session_key()`, drop the `parts[1] != "main"` assertion while keeping a non-empty check to reject malformed keys (`agent::qqbot:...`):

```python
if len(parts) < 5 or parts[0] != "agent" or not parts[1]:
    return None
```
```

## What you have

- `/testbed/repo` is a git clone of `NousResearch/hermes-agent` truncated just after the regression was
  reported.  `HEAD` is `89b38ed734ab2d5c3d263bc24fbdb8c74e931af4` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
