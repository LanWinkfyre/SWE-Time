# Locate the commit that introduced this regression

A regression was reported against `kubernetes/kubernetes`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
List returns nil items field

Behavior of the `items` field for empty lists has changed in 1.5.

With 1.4 (and earlier releases):
```
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "/api/v1/namespaces/default/pods",
    "resourceVersion": "117"
  },
  "items": []
}
```

With 1.5 and master:
```
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "/api/v1/namespaces/default/pods",
    "resourceVersion": "25"
  },
  "items":null
}
```
```

## What you have

- `/testbed/repo` is a git clone of `kubernetes/kubernetes` truncated just after the regression was
  reported.  `HEAD` is `1854d48238b289fa7ac41adfc8dba09cd0f3ce1a` and the full history behind it is present.
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
