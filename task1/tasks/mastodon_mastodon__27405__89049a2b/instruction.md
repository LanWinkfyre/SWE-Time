# Locate the commit that introduced this regression

A regression was reported against `mastodon/mastodon`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Wayback archival broken

### Steps to reproduce the problem

1. Try backing up any mastodon post url with waybackmachines "save page feature"

### Expected behaviour

Proper archival that renders as the original post did

### Actual behaviour

Empty page with no entry

### Detailed description

Attempting to save a mastodon post since mastodons 4.2.0 update results in an empty result archival.
Archive.ph still manages to backup fine.
Example:
https://web.archive.org/web/20231014131443/https://pb.todon.de/@alcea/111233466321909950 vs https://archive.ph/25ZHm

The wayback archive was also informed:
https://pb.todon.de/@alcea/111153855622668345


All mastodon instances running 4.2.x+ are affected

Suggestion for future mastodon releases:
• Ensure compatibility with wayback & archive.ph (perhaps perma.cc too?) to not break this save-ability evermore.
Instances can die. The Wayback is among the few reliable ways to preserve things.



### Mastodon instance

pb.todon.de

### Mastodon version

v4.2.1

### Browser name and version

Firefox 105.0.3

### Operating system

Android 13

### Technical details

_No response_

WBA saves javascript properly, but possibly does a bit of post-processing to make them work properly within an archival context.
```

## What you have

- `/testbed/repo` is a git clone of `mastodon/mastodon` truncated just after the regression was
  reported.  `HEAD` is `e0da64bb4e0ae84fb9380b6e2bff228c997eea62` and the full history behind it is present.
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
