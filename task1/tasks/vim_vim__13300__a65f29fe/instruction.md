# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wrong visual block when selecting wrapped part of lines after a linebreak

### Steps to reproduce


```sh
vim --clean +'set lbr' +'20vsp' - <<END
       aaaaaa bbbbbbbb cccccccc
       aa bbbbb ccccccccc ddddd 
END
```

`:call feedkeys("2E\<C-v>lljr?")`

![2023-10-07-192644_667x301_scrot](https://github.com/vim/vim/assets/16379308/fce272b9-f540-4eda-85e2-0d5b40181474)

undo, reselect the block and move the cursor to the opposite corner
`:call feedkeys("ugvOr?")`

![2023-10-07-192907_667x301_scrot](https://github.com/vim/vim/assets/16379308/4d92f797-21da-440a-93c9-45fe17b57504)



### Expected behaviour

Visual block replace should work like this:

![2023-10-07-194121_667x301_scrot](https://github.com/vim/vim/assets/16379308/97dd9a7d-6427-4ec9-acd7-2d16c7684096)



### Version of Vim



### Environment

Operating System: Archlinux
Terminal: kitty
$TERM: xterm-kitty
shell: bash

### Logs and stack traces

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `2a281ccca017fb5e8ffd20a86aa390431224a2fd` and the full history behind it is present.
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
