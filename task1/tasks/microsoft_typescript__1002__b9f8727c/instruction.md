# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Infinite loop in tsc 1.1.0-1 when compiling code that uses rxjs typings.

Steps:
1. Save this png as a zip file and unpack it:
   ![tsc_infinite_loop zip](https://cloud.githubusercontent.com/assets/1578115/4846978/73e4fcf6-604f-11e4-9319-893cb119ae17.png)
2. Compile `./tsc_infinite_loop/src/client/app/Bind.ts` with the latest version of tsc (1.1.0-1)

ACTUAL: tsc hangs

I marked the line in `Bind.ts` that triggers the bug.

Please feel free to contact me directly if you have any questions, or if you want me to send you the zip file: bparadie at adobe dot com.
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `5ce3baf339e0424263069c70f0ea239bc3cea96a` and the full history behind it is present.
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
