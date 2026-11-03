# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Neovim segfaults

### Neovim version (nvim -v)



### Vim (not Nvim) behaves the same?

no

### Operating system/version

arch

### $TERM environment variable

screen-256color

### Installation

build from repo

### How to reproduce the issue

`:Telescope find_files` crashes neovim. I'll try to find a more minimal reproduction but I can consistently reproduce it with `find_files` .

### Expected behavior

Shouldn't segfault :|

### Actual behavior

Neovim segfaults .


Here's traceback
```log
#0  0xf75b992e in strlen () from /usr/lib/libc.so.6
#1  0xab6085c4 in lj_cf_ffi_string (L=0xf354b5a0) at lib_ffi.c:692
#2  0xab60bf60 in lj_BC_FUNCC ()
#3  0xab60cb14 in lj_ff_coroutine_resume ()
#4  0xab5f8f8c in lua_pcall (L=L@entry=0xf6e9d1c8, nargs=nargs@entry=0,
    nresults=nresults@entry=0, errfunc=errfunc@entry=-2) at lj_api.c:1145
#5  0xab4192d0 in nlua_pcall (lstate=lstate@entry=0xf6e9d1c8, nargs=nargs@entry=0,
    nresults=nresults@entry=0)
    at /home/shadman/projects/neovim/neovim/src/nvim/lua/executor.c:100
#6  0xab41a6e0 in nlua_schedule_event (argv=<optimized out>)
    at /home/shadman/projects/neovim/neovim/src/nvim/lua/executor.c:171
#7  0xab518f40 in state_handle_k_event ()
    at /home/shadman/projects/neovim/neovim/src/nvim/state.c:89
#8  0xab357554 in insert_handle_key (s=s@entry=0xfffeef80)
    at /home/shadman/projects/neovim/neovim/src/nvim/edit.c:1078
#9  0xab3580e4 in insert_execute (state=0xfffeef80, key=<optimized out>)
    at /home/shadman/projects/neovim/neovim/src/nvim/edit.c:838
#10 0xab518df4 in state_enter (s=s@entry=0xfffeef80)
    at /home/shadman/projects/neovim/neovim/src/nvim/state.c:71
#11 0xab34b188 in insert_enter (s=0xfffeef80, s@entry=0xfffeef78)
    at /home/shadman/projects/neovim/neovim/src/nvim/edit.c:494
#12 0xab34b618 in edit (cmdchar=97, startln=startln@entry=false, count=count@entry=1)
    at /home/shadman/projects/neovim/neovim/src/nvim/edit.c:1469
#13 0xab461ba8 in normal_finish_command (s=s@entry=0xfffef024)
    at /home/shadman/projects/neovim/neovim/src/nvim/normal.c:970
#14 0xab46515c in normal_execute (state=0xfffef024, key=<optimized out>)
    at /home/shadman/projects/neovim/neovim/src/nvim/normal.c:1172
#15 0xab518df4 in state_enter (s=0xfffef024, s@entry=0xfffef01c)
    at /home/shadman/projects/neovim/neovim/src/nvim/state.c:71
#16 0xab45b530 in normal_enter (cmdwin=cmdwin@entry=false,
    noexmode=noexmode@entry=false)
    at /home/shadman/projects/neovim/neovim/src/nvim/normal.c:463
#17 0xab4259f0 in main (argc=<optimized out>, argv=<optimized out>)
    at /home/shadman/projects/neovim/neovim/src/nvim/main.c:557
```

@zeertzjq any idea ?
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `a73360a09a54c186f2df6e167a8be1f1a1d8c62a` and the full history behind it is present.
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
