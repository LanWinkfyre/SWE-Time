# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Scrolling the quickfix window causes a freeze

### Steps to reproduce

1. Create the following file:
   `test.vim`

   ```vim
   vim9script
   
   setqflist([
     {"filename": "file1", "text": repeat("A", 200000)},
     {"filename": "file2", "text": repeat("B", 200)}
   ])
   copen
   ```

2. Start Vim with some aruments:

   ```bash
   $ vim --clean -S test.vim
   ```

3. Scroll the quickfix window with `Ctrl-F`

### Actual behavior

Vim freezes for several tens of seconds. (`Ctrl-C` has no effect)
It depends on the performance of PC. On my PC (Win 11, Ryzen 5, 16GB mem), it freezes for 30 seconds.

### Expected behavior

Quickfix window scrolls without freezing.

### Additional info

- `j`, `k` works properly.
- `Ctrl-D`, `Ctrl-U` also freezes.

---

### Result of `git bisect`
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `73440245361f3399b88c872236830da3086ad942` and the full history behind it is present.
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
