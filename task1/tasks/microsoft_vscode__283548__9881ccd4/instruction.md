# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Toggle terminal shorcut stopped working on version 1.107.0-1765353617.el8



<!-- ⚠️⚠️ Do Not Delete This! bug_report_template ⚠️⚠️ -->
<!-- Please read our Rules of Conduct: https://opensource.microsoft.com/codeofconduct/ -->
<!-- 🕮 Read our guide about submitting issues: https://github.com/microsoft/vscode/wiki/Submitting-Bugs-and-Suggestions -->
<!-- 🔎 Search existing issues to avoid creating duplicates. -->
<!-- 🧪 Test using the latest Insiders build to see if your issue has already been fixed: https://code.visualstudio.com/insiders/ -->
<!-- 💡 Instead of creating your report here, use 'Report Issue' from the 'Help' menu in VS Code to pre-fill useful information. -->
<!-- 🔧 Launch with `code --disable-extensions` to check. -->
Does this issue occur when all extensions are disabled?: Yes

<!-- 🪓 If you answered No above, use 'Help: Start Extension Bisect' from Command Palette to try to identify the cause. -->
 The 'Help > Report Issue' dialog can assist with this. -->
- VS Code Version: 1.107.0-1765353617.el8
- OS Version: Fedora Linux 43



Steps to Reproduce:

1. Update to code version 1.107.0-1765353617.el8
2. Press the "Control + `" shortcut to toggle the terminal while in the editor
3. The terminal is not open, instead "`" is typed in the editor

Note that, if the terminal is opened and focused, the "Control + `" shortcut to toggles it correctly.

On version 1.106.3-1764110935.el8 the same shortcut toggled the terminal correctly.

@ulugbekna I’m on AlmaLinux 9.7.



There are no errors in the console.

One thing that might help: the shortcut works when I use the default US keyboard layout (no dead keys), but it does not work with the US layout that has dead keys enabled.

Here are two shortcut logs:
With dead keys (not working): 
```
2026-01-30 11:49:16.109 [info] [Window] [KeybindingService]: / Soft dispatching keyboard event
2026-01-30 11:49:16.110 [info] [Window] [KeybindingService]: \ Keyboard event cannot be dispatched
2026-01-30 11:49:16.111 [info] [Window] [KeybindingService]: / Received  keydown event - modifiers: [ctrl], code: ControlLeft, keyCode: 17, key: Control
2026-01-30 11:49:16.111 [info] [Window] [KeybindingService]: | Converted keydown event - modifiers: [ctrl], code: ControlLeft, keyCode: 5 ('Ctrl')
2026-01-30 11:49:16.112 [info] [Window] [KeybindingService]: \ Keyboard event cannot be dispatched in keydown phase.
2026-01-30 11:49:16.709 [info] [Window] [KeybindingService]: / Soft dispatching keyboard event
2026-01-30 11:49:16.710 [info] [Window] [KeybindingService]: | Resolving ctrl+[Backquote]
2026-01-30 11:49:16.711 [info] [Window] [KeybindingService]: \ From 1 keybinding entries, matched workbench.action.terminal.toggleTerminal, when: terminal.active, source: built-in.
2026-01-30 11:49:17.803 [info] [Window] [KeybindingService]: + Ignoring single modifier ctrl due to it being pressed together with other keys.
```

Without dead keys (working): 
```
2026-01-30 11:48:34.717 [info] [Window] [KeybindingService]: / Soft dispatching keyboard event
2026-01-30 11:48:34.718 [info] [Window] [KeybindingService]: \ Keyboard event cannot be dispatched
2026-01-30 11:48:34.719 [info] [Window] [KeybindingService]: / Received  keydown event - modifiers: [ctrl], code: ControlLeft, keyCode: 17, key: Control
2026-01-30 11:48:34.720 [info] [Window] [KeybindingService]: | Converted keydown event - modifiers: [ctrl], code: ControlLeft, keyCode: 5 ('Ctrl')
2026-01-30 11:48:34.721 [info] [Window] [KeybindingService]: \ Keyboard event cannot be dispatched in keydown phase.
2026-01-30 11:48:35.107 [info] [Window] [KeybindingService]: / Soft dispatching keyboard event
2026-01-30 11:48:35.108 [info] [Window] [KeybindingService]: | Resolving ctrl+[Backquote]
2026-01-30 11:48:35.108 [info] [Window] [KeybindingService]: \ From 1 keybinding entries, matched workbench.action.terminal.toggleTerminal, when: terminal.active, source: built-in.
2026-01-30 11:48:35.109 [info] [Window] [KeybindingService]: / Received  keydown event - modifiers: [ctrl], code: Backquote, keyCode: 192, key: Unidentified
2026-01-30 11:48:35.110 [info] [Window] [KeybindingService]: | Converted keydown event - modifiers: [ctrl], code: Backquote, keyCode: 91 ('`')
2026-01-30 11:48:35.111 [info] [Window] [KeybindingService]: | Resolving ctrl+[Backquote]
2026-01-30 11:48:35.111 [info] [Window] [KeybindingService]: \ From 1 keybinding entries, matched workbench.action.terminal.toggleTerminal, when: terminal.active, source: built-in.
2026-01-30 11:48:35.112 [info] [Window] [KeybindingService]: + Invoking command workbench.action.terminal.toggleTerminal.
2026-01-30 11:48:35.245 [info] [Window] [KeybindingService]: / Soft dispatching keyboard event
2026-01-30 11:48:35.245 [info] [Window] [KeybindingService]: | Resolving ctrl+[Backquote]
2026-01-30 11:48:35.246 [info] [Window] [KeybindingService]: \ From 1 keybinding entries, matched workbench.action.terminal.toggleTerminal, when: terminal.active, source: built-in.
2026-01-30 11:48:36.068 [info] [Window] [KeybindingService]: / Soft dispatching keyboard event
2026-01-30 11:48:36.069 [info] [Window] [KeybindingService]: \ Keyboard event cannot be dispatched
2026-01-30 11:48:36.070 [info] [Window] [KeybindingService]: + Ignoring single modifier ctrl due to it being pressed together with other keys.
```
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `a7cfff7ea03e94f9dade0742980de36fc56848a1` and the full history behind it is present.
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
