# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Links using @ref stopped working in doxygen 1.8.19

**Describe the bug**
In wxWidgets interface documentation, `@ref` is used to link to reference a different class in the documentation.  It appears that in doxygen 1.8.19, these links stopped being generated correctly.  

**Expected behavior**
These are how the links look in doxygen 1.8.18 (correct):
```
$ grep -rsI "For more information on socket events" *
out/html/classwx_socket_base.html: For more information on socket events see <a class="el" href="socket_8h.html#wxSocketFlags">wxSocketFlags</a> . </li>
out/html/classwx_socket_base.html:<p>For more information on socket events see <a class="el" href="socket_8h.html#wxSocketEventFlags">wxSocketEventFlags</a> . </p>
```

**Screenshots**
This is how the links look in doxygen 1.8.19:
```
[talbert@deasil doxygen]$ grep -rsI "For more information on socket events" *
out/html/classwx_socket_base.html: For more information on socket events see <a class="el" href="/home/talbert/Downloads/dox_repro/interface/wx/socket.h#wxSocketFlags">wxSocketFlags</a> . </li>
out/html/classwx_socket_base.html:<p>For more information on socket events see <a class="el" href="/home/talbert/Downloads/dox_repro/interface/wx/socket.h#wxSocketEventFlags">wxSocketEventFlags</a> . </p>
```

**To Reproduce**
[doxygen.tar.gz](https://github.com/doxygen/doxygen/files/5233522/doxygen.tar.gz)

**Version**
1.8.18 works, 1.8.19+ doesn't.
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `0fc06d657d596adcc289a5f228973ea268efd66d` and the full history behind it is present.
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
