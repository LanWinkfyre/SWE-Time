# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wrong cursor position when breakindent and linebreak are both enabled

### Steps to reproduce


```bash
vim --clean +'set bri lbr' - +40vsp <<END
	a aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa*aaaaaaa!bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb*bbbbbbb!ccccccccccccccccccccccccccccccc*ccccccc!dddd
	aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa*aaaaaaa!bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb*bbbbbbb!ccccccccccccccccccccccccccccccc*ccccccc!dddd
END
```
feed keys: `f*lll<C-V>llrQ`

![2023-08-28-001649_1121x736_scrot](https://github.com/vim/vim/assets/16379308/b0c5e8a8-5e69-464f-b5a6-648bbe95cdba)

As you can see the cursor goes over some virtual whitespace after the first '*'.



### Expected behaviour

Cursor should not be positioned over the virtual whitespace.

### Version of Vim

latest master @ 9.0.1811

### Environment

Operating system: ArchLinux
Terminal: kitty
Value of $TERM: xterm-kitty
Shell: Bash

### Logs and stack traces

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `85c3a5bc265393c1b8b93d8b88b936d3b8b4aec7` and the full history behind it is present.
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
