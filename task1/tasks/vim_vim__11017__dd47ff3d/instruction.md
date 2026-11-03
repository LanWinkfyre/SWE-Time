# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[bisected] Screen flickers and leaves artifacts when cmdheight=0 and changing background from plugin

### Steps to reproduce

1. Download and extract the minimal reproducing example [background-plug.tar.gz](https://github.com/vim/vim/files/9455502/background-plug.tar.gz) so that the plugin resides in `/tmp/background-plug` and the following two files (included in the archive) are present at `/tmp/background-plug/colors/background-plug.vim` and `/tmp/background-plug/plugin/background-plug.vim`:
```vim
" colors/background-plug.vim
hi clear
if exists("syntax_on")
	syntax reset
endif
let g:colors_name = "background-plug"

if &background == 'light'
	hi Normal guifg=#000000 guibg=#ffffff
else
	hi Normal guifg=#ffffff guibg=#000000
endif
```
```vim
" plugin/background-plug.vim
if 0
	echom "this if condition is important for the bug to trigger, even though it is never run"
endif

set background=dark
```
2. Start vim with the following configuration:
```bash
src/vim --clean -Nu <(cat<<EOF
set termguicolors
set background=light
set cmdheight=0
set rtp+=/tmp/background-plug
colorscheme background-plug
EOF
)
```

The screen will flicker when you start up vim similar to https://github.com/neovim/neovim/issues/19362, and when you quit vim, it will leave artifacts of the last vim buffer visible on the terminal.

### Expected behaviour

The screen should not flicker at startup and vim should not leave artifacts on the screen when quitting.



### Version of Vim

9.0.0333

### Environment

Operating System: Arch Linux
Terminal: Wezterm with $TERM=xterm-256color
Shell: zsh

### Logs and stack traces

A screen recording of the issue is visible at: https://asciinema.org/a/Ti1DU8g8jpppfOTSCJGYg3xs7
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `f240395fca63d4b330112a4b81e94b05b50de1aa` and the full history behind it is present.
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
