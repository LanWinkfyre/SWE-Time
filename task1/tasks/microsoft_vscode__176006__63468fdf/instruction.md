# Locate the commit that introduced this regression

A regression was reported against `microsoft/vscode`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Latest release of VSCode (1.76.0) breaks first party extensions including "WAVE for Windows"

looks related to "I cannot build my VSCode extension project in VSCode after update to 1.76"  Issue #175833 



Typically, when a dev opens a folder in the OS repo, the Wave extension is activated and begins to initialize and 'restore dependencies', by running a few scripts, setting up the build environment.  in >= 1.76.0, we briefly see "Activating extensions..." in the status bar then it abruptly stops. 

•	Windows developers on release 1.76.0 have been unable to do their work in VSCode since the release 
•	When users revert to version 1.75, the issues don't happen anymore; the extension is activated, scripts run, and the environment is properly prepared.

What we know so far: 
•	Our WAVE extension is loaded, at least momentarily and initialization begins, but fails and exits fairly early on
o	Per the comment from the GitHub issue above, we listened for error messages in devtools (Help > Toggle Developer Tools)
o	VSCode output has very few details in the log, and not very helpful to debug
o	Our wave extension architect tried debugging and noticed that the build does not complete. VSCode attempts to launch WAVE but then sharply exits the process with no indication in the debugger for what is happening under the hood.
 No log info in debugger that indicates why the “Activating extensions” process quits.

Results of npx vscode-bisect:
 » **Bad**
    ...
     » **Good**
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/vscode` truncated just after the regression was
  reported.  `HEAD` is `8354eaa91c05d25dd79da068e8a57b6849a24461` and the full history behind it is present.
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
