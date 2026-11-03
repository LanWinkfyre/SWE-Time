# Locate the commit that introduced this regression

A regression was reported against `vim/vim`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Error detected while processing function <SNR>39_Highlight_Matching_Pair:    in bash file

The title error message appears when the cursor moves between curly brackets in a bash file. The file contains  ' { } '.  ( There are four characters)



==========================
steps to duplicate:
1. echo " ' {} ' " > /tmp/2.sh
2.  src/vim /tmp/2.sh
3. cross the cursor '{' and '}' by moving left to right. error appears


===========================
details error:
Error detected while processing function <SNR>39_Highlight_Matching_Pair:                                              
line   78:
E475: Invalid argument: 0

===========================
```

## What you have

- `/testbed/repo` is a git clone of `vim/vim` truncated just after the regression was
  reported.  `HEAD` is `218beb3e96bcb7b20395be3bec6076c767be71a1` and the full history behind it is present.
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
