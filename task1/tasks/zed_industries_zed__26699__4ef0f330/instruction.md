# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Crash when cisco anyconnect VPN connects or disconnects

### Summary

<!-- Please insert a one line summary of the issue below -->
In the past two weeks or so, I noticed Zed crashes when my VPN (cisco anyconnect) connects or disconnects.
<!-- Include all steps necessary to reproduce from a clean Zed installation. Be verbose -->
Steps to trigger the problem:
1. Open and use Zed as usual
2. Connect to VPN using the cisco anyconnect client
3. Zed crashes immediately after VPN connects (the Mac OS prompts something like "do you want to reopen Zed?")

Actual Behavior:
This kind of crash happens any time when my VPN status changes, either connect or disconnect. I assume some kind of network changes triggered this crash.
And also to be clear, when it crashes, I am not connecting to any remote files requiring VPN. Only local files were opened in Zed upon the crash.


Expected Behavior:
Zed should behave normally regardless of my VPN status.

### Zed Version and System Specs

Zed: v0.177.8 (Zed) 
OS: macOS 15.3.2
Memory: 128 GiB
Architecture: aarch64

### If applicable, attach your `~/Library/Logs/Zed/Zed.log` file to this issue.

<details><summary>Zed.log</summary>

<!-- Click below this line and paste or drag-and-drop your log-->
```

```
<!-- Click above this line and paste or drag-and-drop your log--></details>


Ok, I found this commit introduced the issue:




<details>
  <summary>The full `git bisect` logs</summary>


</details>

<details>



</details>
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `18fcdf1d2c00d21ef6d1ccd8d771bd956cdb9687` and the full history behind it is present.
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
