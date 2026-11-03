# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Inspector buttons are missing padding on the right side

### Godot version



### System information

Windows 10

### Issue description

Inspector buttons are missing padding on the right side of the text.

| Alpha 13 | Alpha 14 |
---|---
| ![image](https://user-images.githubusercontent.com/67974470/184504374-8cef0821-cdd4-4d17-a619-8ff10f2b2905.png) | ![image](https://user-images.githubusercontent.com/67974470/184504282-ce62bc3f-7fc0-40e3-b7a8-6e898463f622.png) |
| ![image](https://user-images.githubusercontent.com/67974470/184504385-92c77f80-3b23-463b-96c9-1b6dd7ecb9a6.png) | ![image](https://user-images.githubusercontent.com/67974470/184504313-f6e7a273-1460-47a0-a215-615e07842259.png) |
| ![image](https://user-images.githubusercontent.com/67974470/184504392-47e51e15-a0d0-494d-b0ac-61a29b0fb6cd.png) | ![image](https://user-images.githubusercontent.com/67974470/184504333-7d2051a8-e937-4482-b0e6-f286024016bd.png) |

### Steps to reproduce

* Select a node.
* Look at the Add Metadata button at the bottom of the inspector.

### Minimal reproduction project

_No response_

 This can be seen in the project manager when the Remove Missing button is visible in the sidebar:

![image](https://user-images.githubusercontent.com/180032/184509272-a8721221-ba04-4e64-ab87-d2193acdbca4.png)

4.0.alpha13 doesn't have this issue:

![image](https://user-images.githubusercontent.com/180032/184509319-0c8ab275-59c9-4270-8e76-55f170403d84.png)

I'm bisecting the issue.
 cc @KoBeWi
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `f2a61684143af02a8cbe7002645af817607f9bd6` and the full history behind it is present.
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
