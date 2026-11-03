# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
SIGSEGV when case-folding invalid char

### Problem

Neovim reliably segfaults while attempting to draw a window for the first time.

### Steps to reproduce

I have been unable to create a minimal reproducer for now. The crash seems to rely on both my config and vim-polyglot and AFAICT only requires running `:TOhtml` on a file with zsh syntax highlighting to reproduce. I will keep attempting to build a reproducer, if I can't fix it myself.

### Expected behavior

No crash.


### Additional information
Backtrace:
```
0x000055f26b256338 in utf_ptr2char (p_in=0x0) at /home/me/prog/neovim/src/nvim/mbyte.c:673
673       uint32_t const v0 = p[0];
(ins)(gdb) bt
#0  0x000055f26b256338 in utf_ptr2char (p_in=0x0) at /home/me/prog/neovim/src/nvim/mbyte.c:673
#1  0x000055f26b257613 in utf_fold (a=55296) at /home/me/prog/neovim/src/nvim/mbyte.c:1314
#2  0x000055f26b31686c in nfa_regmatch (prog=0x55f27cc8e770, start=0x55f27cc8eba8, 
    submatch=0x7fff2dfe3230, m=0x7fff2dfe3390) at /home/me/prog/neovim/src/nvim/regexp.c:14810
#3  0x000055f26b318c4a in nfa_regtry (prog=0x55f27cc8e770, col=24, tm=0x7fff2dfe5200, 
    timed_out=0x7fff2dfe36f8) at /home/me/prog/neovim/src/nvim/regexp.c:15535
#4  0x000055f26b319431 in nfa_regexec_both (
    line=0x55f27cc2375f "body {background-color: #ffffff; color: #4e4e4e}", startcol=4, 
    tm=0x7fff2dfe5200, timed_out=0x7fff2dfe36f8) at /home/me/prog/neovim/src/nvim/regexp.c:15720
#5  0x000055f26b3198a5 in nfa_regexec_multi (rmp=0x7fff2dfe3810, win=0x55f27c7b5aa0, buf=0x55f27cc1d780, 
    lnum=9, col=4, tm=0x7fff2dfe5200, timed_out=0x7fff2dfe36f8)
    at /home/me/prog/neovim/src/nvim/regexp.c:15926
#6  0x000055f26b31a138 in vim_regexec_multi (rmp=0x7fff2dfe3810, win=0x55f27c7b5aa0, buf=0x55f27cc1d780, 
    lnum=9, col=4, tm=0x7fff2dfe5200, timed_out=0x7fff2dfe36f8)
    at /home/me/prog/neovim/src/nvim/regexp.c:16201
#7  0x000055f26b379af4 in syn_regexec (rmp=0x7fff2dfe3810, lnum=9, col=4, st=0x55f27cddbdb0)
    at /home/me/prog/neovim/src/nvim/syntax.c:2683
#8  0x000055f26b3776ec in syn_current_attr (syncing=false, displaying=true, can_spell=0x0, 
    keep_state=false) at /home/me/prog/neovim/src/nvim/syntax.c:1665
#9  0x000055f26b376f06 in get_syntax_attr (col=4, can_spell=0x0, keep_state=false)
    at /home/me/prog/neovim/src/nvim/syntax.c:1465
#10 0x000055f26b10168b in win_line (wp=0x55f27c7b5aa0, lnum=9, startrow=8, endrow=13, col_rows=0, 
    spv=0x7fff2dfe5240, 
    foldinfo={fi_lnum = 426209280, fi_level = 0, fi_low_level = 1801804264, fi_lines = 0})
    at /home/me/prog/neovim/src/nvim/drawline.c:1970
#11 0x000055f26b10a5ed in win_update (wp=0x55f27c7b5aa0)
    at /home/me/prog/neovim/src/nvim/drawscreen.c:2249
#12 0x000055f26b105ca6 in update_screen () at /home/me/prog/neovim/src/nvim/drawscreen.c:639
#13 0x000055f26b2888fb in normal_redraw (s=0x7fff2dfe53e0) at /home/me/prog/neovim/src/nvim/normal.c:1355
#14 0x000055f26b288b87 in normal_check (state=0x7fff2dfe53e0)
    at /home/me/prog/neovim/src/nvim/normal.c:1457
#15 0x000055f26b365add in state_enter (s=0x7fff2dfe53e0) at /home/me/prog/neovim/src/nvim/state.c:40
#16 0x000055f26b286760 in normal_enter (cmdwin=false, noexmode=false)
    at /home/me/prog/neovim/src/nvim/normal.c:520
#17 0x000055f26b22b3da in main (argc=4, argv=0x7fff2dfe57c8) at /home/me/prog/neovim/src/nvim/main.c:661
```


### Neovim version (nvim -v)



### Vim (not Nvim) behaves the same?

N/A

### Operating system/version

Linux r4 6.10.7-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.10.7-1 (2024-08-31) x86_64 GNU/Linux

### Terminal name/version

kitty 0.36.1 created by Kovid Goyal

### $TERM environment variable

xterm-kitty

### Installation

built from source/appimage
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `a0d8c2b86e788ce4273f0b8df258cd9e8e432d38` and the full history behind it is present.
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
