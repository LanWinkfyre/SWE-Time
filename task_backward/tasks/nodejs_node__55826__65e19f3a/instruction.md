# Locate the commit that introduced this regression

A regression was reported against `nodejs/node`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
23.2 breaks a few packages that use json trough webpack (date-fns)

### Version

v23.2.0

### Platform

```text
Linux arch 6.11.6-zen1-1-zen #1 ZEN SMP PREEMPT_DYNAMIC Fri, 01 Nov 2024 03:30:35 +0000 x86_64 GNU/Linux
```


### Subsystem

_No response_

### What steps will reproduce the bug?

Use a package that includes for example date-fns on a NextJS project.

### How often does it reproduce? Is there a required condition?

100%

### What is the expected behavior? Why is that the expected behavior?

To build

### What do you see instead?

```
 npm run build

> next build

   ▲ Next.js 15.0.3
   - Environments: .env

 ✓ Linting and checking validity of types    
   Creating an optimized production build ...
Failed to compile.

./node_modules/react-remove-scroll/dist/es2015/Combination.js + 22 modules
Unexpected end of JSON input

./node_modules/date-fns/format.js + 21 modules
Unexpected end of JSON input

./node_modules/date-fns/locale/fr.js + 5 modules
Unexpected end of JSON input


> Build failed because of webpack errors
```

### Additional information

Seems to be a newly arrived issue only for 23.2.

Tested with 23.1 and 23.0 with no issue.
```

## What you have

- `/testbed/repo` is a git clone of `nodejs/node` truncated just after the regression was
  reported.  `HEAD` is `03d414ed9add84541e71d180fed1b7b0609ff6c8` and the full history behind it is present.
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
