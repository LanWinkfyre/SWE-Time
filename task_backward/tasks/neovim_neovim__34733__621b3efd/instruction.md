# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Half-width katakana and voicing mark causes corrupted TUI after v0.11.0

### Problem

In Japanese, half-width katakana and voicing mark are displayed in 2 characters wide, and Neovim also showed them as expected too. However, it is not the case with Neovim v0.11.0 and after.

The problem is, terminals show them as two-characters wide. It causes visual corruption in many ways. The following screenshot illustrates how it affects `colorcolumn`.

![Image](https://github.com/user-attachments/assets/eaf40029-89bf-4528-8ceb-8a09688e0922)

In a real-world text file, the wrong display width often causes unexpected soft wrap and results in TUI corruption on every scroll... just unusable.

Note that the screenshots are Neovim on WSL2 on Windows Terminal, but I confirmed that Neovim with iTerm2 on macOS behaves wrongly as well. Also note that the Windows Terminal itself wrongly renders voicing mark (the mark should be right after character), but it's a separate problem.

For reference, this is how VS Code renders them:

![Image](https://github.com/user-attachments/assets/0bad52f9-a4ca-4ae1-88cd-048fe9fb8cc8)

In addition, `strdisplaywidth('ｶﾞ')` is `2` on v0.10.4 but `1` on v0.11.0.

---

I checked several versions:

- OK: nvim v0.10.4, vim 0.9.1500


### Steps to reproduce

1. Create a file containing the following contents, namely `halfkana.txt`
  ```
  ｱｲｳｴｵ
  ｶﾞｷﾞｸﾞｹﾞｺﾞ
  ﾊﾟﾋﾟﾌﾟﾍﾟﾎﾟ
  
  
  vim: set colorcolumn=15:
  ```
2. `nvim --clean halfkana.txt`
3. Notice the corruption.
4. `echo strdisplaywidth('ｶﾞ')` and see `1`.

### Expected behavior

- Katakana is shown as in v0.10.4.
- `echo strdisplaywidth('ｶﾞ')` returns `2`.

### Nvim version (nvim -v)

NVIM v0.11.0

### Vim (not Nvim) behaves the same?

No, 0.9.1500

### Operating system/version

Ubuntu 22.04 (WSL 2)

### Terminal name/version

Windows Terminal 1.23.11132.0 & tmux

### $TERM environment variable

screen-256color

### Installation

Linuxbrew
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `807bc00dd68dccb55d5aa12e0a568d2551b08d04` and the full history behind it is present.
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
