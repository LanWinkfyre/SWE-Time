# Locate the commit that introduced this regression

A regression was reported against `neovim/neovim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Garbage output in stderr after quitting nvim --clean, regressed since 0.9.5

### Problem

Full MWE:
```python
import subprocess
import os

editor = os.environ['EDITOR']
command = [editor, "foo.txt"]
proc = subprocess.Popen(command, stderr=subprocess.PIPE, encoding='utf-8')
_stdout, stderr = proc.communicate()
print(stderr)
```

Regression:
```
$ EDITOR=nvim python sample.py

^[]11;rgb:fbfb/f1f1/c7c7^[\⏎                            
$ 11;rgb:fbfb/f1f1/c7c7
```

Expected:
```
$ EDITOR=vim python sample.py
<no output>
```

Smaller test bench showing stderr output when using `nvim --clean`:
```
nvim --clean +qa 2> stderr.log && cat stderr.log
+q5463;524742;73657472676266;73657472676262$qm^[]11;rgb:ffff/ffff/ffff^G⏎                                                                                                
$ 11;rgb:ffff/ffff/ffff    
```

There is garbage output in stderr where there wasn't before.

Scripts that work with $EDITOR and capture stderr will have problems interpreting this since it seems to contain some escape codes.

### Steps to reproduce

nvim --clean +qa 2> stderr.log && cat stderr.log

### Expected behavior

There should be no output. I verified on 0.9.5:
```
~ ❯ bob use 0.9.5 && nvim --clean +qa 2> stderr.log && cat stderr.log
Mar 06 11:08:56.136  INFO You can now use v0.9.5!

```

### Nvim version (nvim -v)



### Vim (not Nvim) behaves the same?

no, vim 9.1

### Operating system/version

macOS

### Terminal name/version

Terminal.app, Wezterm 20240203-110809-5046fc22, Ghostty 1.1.2

### $TERM environment variable

xterm-256color

### Installation

bob
```

## What you have

- `/testbed/repo` is a git clone of `neovim/neovim` truncated just after the regression was
  reported.  `HEAD` is `7371abf7554ebbcdb66bde3c892954596c497ff4` and the full history behind it is present.
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
