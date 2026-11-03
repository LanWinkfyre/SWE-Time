# Locate the commit that introduced this regression

A regression was reported against `grafana/grafana`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Transformations: "Convert field type" ignores dateFormat for string fields

### What happened?

The `Convert field type` transformation ignores the configured `dateFormat` when the input field holds **strings**. Any all-digit string is now interpreted as a Unix epoch **millisecond** value regardless of the format the user configured.

A field configured with `destinationType: "time"` and `dateFormat: "X"` (Unix seconds) produces dates in January 1970 instead of the expected timestamps.







**This is broader than `X`.** Every numeric-only format is affected — `X`, `x`, `YYYYMMDD`, `YYYYMMDDHHmmss`.

| Input | `dateFormat` | Result on `main` | Expected |
| --- | --- | --- | --- |
| `"1700000000"` (string) | `X` | `1970-01-20T16:13:20Z` | `2023-11-14T22:13:20Z` |
| `1700000000` (number) | `X` | `2023-11-14T22:13:20Z` | `2023-11-14T22:13:20Z` |
| `"20240115"` (string) | `YYYYMMDD` | `1970-01-01T05:37:20.115Z` | `2024-01-15T00:00:00Z` |

### What did you expect to happen?

String inputs should be parsed according to the configured `dateFormat`, as the [Convert field type documentation](https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/transform-data/#convert-field-type) describes. Only numeric inputs should be treated as epoch milliseconds.

### Did this work before?

Yes.  In practical terms this currently reaches Grafana Cloud and nightly builds, and will ship with 13.2.0 unless fixed first.

### How do we reproduce it?

1. Create a panel with a query returning a **string** field of Unix second timestamps, e.g. `"1700000000"` (the TestData `CSV Content` scenario works).
2. Add a `Convert field type` transformation.
3. Set the field's destination type to `Time` and the date format input to `X`.
4. The resulting timestamps land in January 1970 rather than 2023.

Equivalent unit-level reproduction:

```ts
const field = toDataFrame({
  fields: [{ name: 'ts', type: FieldType.string, values: ['1700000000'] }],
}).fields[0];

fieldToTimeField(field, 'X').values; // [1700000000] — expected [1700000000000]
```







### Is the bug inside a dashboard panel?

Yes — `Convert field type` transformation.

### Environment (with versions)?

Grafana: `main` / `13.2.0-pre` (also affects Grafana Cloud). Not present in 13.1.x, 13.0.x, or 12.x.

### Grafana platform?

Grafana Cloud, and any build from `main`.

### Datasource(s)?

Datasource-agnostic — the defect is in the frontend transformation.
```

## What you have

- `/testbed/repo` is a git clone of `grafana/grafana` truncated just after the regression was
  reported.  `HEAD` is `e6cf001c19890a110b4f2677776988793d02f14a` and the full history behind it is present.
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
