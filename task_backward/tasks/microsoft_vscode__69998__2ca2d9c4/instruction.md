# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Open vscode://file/<path> in vscode is broken

<!-- Please search existing issues to avoid creating duplicates. -->
<!-- Also please test using the latest insiders build to make sure your issue has not already been fixed: https://code.visualstudio.com/insiders/ -->

<!-- Use Help > Report Issue to prefill these. -->
- VSCode Version:
`code --version`
1.32.0

x64

- OS Version:
macOS High Sierra v10.13.6 (17G3025)

Steps to Reproduce:

1. In terminal `open vscode://file/<my_file_path>`
2. It will popup notification with error `Unable to open '<my_file>': resource is not available.`

<!-- Launch with `code --disable-extensions` to check. -->
Does this issue occur when all extensions are disabled?: Yes

Since I tried same url just changed `vscode` to `vscodium` and VSCodium v1.13.1 works perfectly
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `7333aa8aee07946b2f4906a17ec6ce7e95b5155b` and the full history behind it is present.
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
