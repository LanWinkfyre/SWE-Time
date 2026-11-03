# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Vim unusable after compile with tiny features

### Steps to reproduce

```
docker run --rm -it alpine
apk add --no-cache gcc make musl-dev ncurses-static git
git clone https://github.com/vim/vim /opt/vim
cd /opt/vim
LDFLAGS="-static" ./configure --with-features=tiny --with-tlib=ncursesw
make
make install

vim
```

Vim is unusable in this state. Only one character per line. Weird interface issues.



 Everything before that doesn't have this problem.

### Expected behaviour

Vim should be usable out-of-the-box without any issues after compilation.

### Version of Vim

Latest
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `ef818ae4448726b91c31e24406a554686dea19f5` and the full history behind it is present.
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
