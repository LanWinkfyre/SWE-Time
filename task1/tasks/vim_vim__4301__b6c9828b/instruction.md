# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wonky mouse in rxvt-unicode after vim upgrade (regression)

Hi,

After recently updating vim the mouse is all messed up for me on rxvt-unicode, causing really large amounts of unwanted scrolling when selecting text while holding shift.

To reproduce, create a file large enough to scroll (/tmp/spew in example), then:

    % yes | head -n1000 >/tmp/spew
    % vim -N -u NONE /tmp/spew
    :set mouse=a

Then scroll to the end, hold shift, and click+drag anywhere in an attempt to select some text in the terminal.  While dragging, the screen scrolls up (and only up) whenever the mouse is moving, moving very quickly to the top of the file.  This makes it essentially impossible to select any text with this method, unless it can be selected with the file scrolled all the way to the beginning.

Bisection implicates this patch as causing the problem:
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `725310d89e1ba268bf410472b7de054c6c260161` and the full history behind it is present.
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
