# Locate the commit that introduced this regression

A regression was reported against `ClickHouse/ClickHouse`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
LOGICAL_ERROR: Format {} doesn't support schema inference



```
SELECT [''], ( SELECT * FROM file('') ) , ( SELECT * FROM cosn('', 8.7) ) , (CAST(([]) AS DateTime))
```

Error in 24.6:
```
Code: 715. DB::Exception: The data format cannot be detected by the contents of the files. You can specify the format manually: (in file/uri /mnt/ch/ClickHouse/). (CANNOT_DETECT_FORMAT)
```

Error in master:
```
Received exception:
Code: 636. DB::Exception: The table structure cannot be extracted from a Markdown format file. Error:
Code: 49. DB::Exception: FormatFactory: Format Markdown doesn't support schema inference. (LOGICAL_ERROR) (version 24.7.1.1).
You can specify the structure manually: (in file/uri /mnt/ch/ClickHouse/.git-blame-ignore-revs). (CANNOT_EXTRACT_TABLE_STRUCTURE)
```
```

## What you have

- `/testbed/repo` is a git clone of `ClickHouse/ClickHouse` truncated just after the regression was
  reported.  `HEAD` is `217363d9a766bacbf0acae88118dff1055dbbaa9` and the full history behind it is present.
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
