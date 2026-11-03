# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
view unexpectedly altered when 'winminheight' is 0


 - `vim -u DEFAULTS` (version:  8.1 Included patches: 1-2231) behaves differently? Yes
 - Operating system/version: Ubuntu 16.04.6 LTS
 - Terminal name/version: XTerm(322)
 - `$TERM`: xterm-256color

### Steps to reproduce

Run this shell command:

    nvim -Nu NONE +'set wmh=0 | au WinEnter * wincmd _' +'sp|$' <(curl -Ls https://raw.githubusercontent.com/neovim/neovim/master/LICENSE)

Then, press `C-w w` twice.

### Actual behaviour

The view of the top window has changed. Before pressing `C-w w` twice, the topline was `252` (output of `:echo getwininfo()[0].topline`); now it's `281`.

![gif](https://user-images.githubusercontent.com/8505073/67738442-edf12200-fa0e-11e9-9414-827b38889cd6.gif)

### Expected behaviour

The view is preserved; i.e. the topline stays the same.

### Additional information

In Vim, the view is preserved:

![gif](https://user-images.githubusercontent.com/8505073/67738487-33155400-fa0f-11e9-91f6-1b52fc785ba4.gif)

---

If `'winminheight'` is set to a value different than 0, the view is preserved.

---

I searched for the keywords `winminheight` and `squash` in the commit messages of Vim patches, but couldn't find anything which seems relevant (there is [`7.4.372`](https://github.com/vim/vim/releases/tag/v7.4.372) but it's absent from the output of `./scripts/vim-patch.sh -l`).
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `83b6d9f197a44e3b8140619e6b7e9950f217aafb` and the full history behind it is present.
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
