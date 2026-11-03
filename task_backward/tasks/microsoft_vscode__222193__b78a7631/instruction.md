# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TypeError: Failed to execute 'createPolicy' on 'TrustedTypePolicyFactory': Policy with name "defaultWorkerFactory" already exists.

I see this error a lot in the VS Code insider dev tools:

![Image](https://github.com/user-attachments/assets/0e0b2b09-5aec-4d44-8f6a-a705780cd998)

![Image](https://github.com/user-attachments/assets/c5048019-b01e-424c-8a7c-20cc0e56cc90)



Bisect points to the following,



 Fun fact the duplicate policy creation is not raised when performing the same actions in a nested worker, possibly a bug in Chrome. Simple repro, https://gist.github.com/deepak1556/3e9d238c0d70c07dd23595df09152f25
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `37898a5689f24f6fb14e4942eb2a18ead0eb4358` and the full history behind it is present.
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
