# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
sql/tests: TestCreateRandomSchema failed




```
=== RUN   TestCreateRandomSchema
    test_log_scope.go:165: test logs captured to: outputs.zip/logTestCreateRandomSchema477618548
    test_log_scope.go:76: use -show-logs to present logs inline
    random_schema_test.go:107: for input statement
        CREATE TABLE table74 (col74_0 BPCHAR NOT NULL, col74_1 STRING, col74_2 INT8 NOT NULL, col74_3 INT8 NOT NULL, col74_4 INTERVAL NOT NULL, col74_5 INT4 NOT NULL, col74_6 BOX2D NOT NULL, col74_7 INT4 NOT NULL AS (abs(col74_5)) STORED, col74_8 INT8 NOT NULL AS (abs(col74_3)) STORED, col74_9 INT8 NOT NULL AS ((col74_3 + col74_2) + col74_5) VIRTUAL, col74_10 INT8 NOT NULL AS (col74_2 + col74_5) VIRTUAL, col74_11 STRING NOT NULL AS (lower(CAST(col74_6 AS STRING))) VIRTUAL, col74_12 INT8 NOT NULL AS (abs(col74_3)) VIRTUAL, PRIMARY KEY (col74_10 ASC, col74_6 ASC, col74_4 DESC), UNIQUE (col74_9 ASC, col74_0 DESC, col74_12 ASC, col74_1 DESC, col74_4 ASC, col74_6, col74_7 DESC, col74_11), INDEX (col74_8, col74_2 ASC, col74_0, col74_1 DESC, col74_7 DESC, col74_4, col74_3, col74_5, col74_12 DESC, col74_10 DESC), UNIQUE (col74_3), UNIQUE (col74_11 DESC, col74_0 ASC, col74_2 ASC) PARTITION BY LIST (col74_11, col74_0, col74_2) (PARTITION table74_part_0 VALUES IN ((e'(\x0e\n]':::STRING, ' ':::STRING, 719093526511692457:::INT8), (e'\x11\x19Q#7]':::STRING, '(':::STRING, 5274592778260151416:::INT8)), PARTITION table74_part_1 VALUES IN ((e'4U_f>\x7f\x03+':::STRING, e'\r':::STRING, 2208581895336924722:::INT8), ('jV@_':::STRING, e'\x02':::STRING, (-2812879838062368897):::INT8)), PARTITION table74_part_2 VALUES IN ((e'\x11\x06N\x14\x11':::STRING, 'u':::STRING, 2370269809838248347:::INT8), (e'\x1e"':::STRING, '3':::STRING, 127:::INT8)), PARTITION table74_part_3 VALUES IN ((e'\x0eW\x0eG88\'\x05\x1f':::STRING, 'Y':::STRING, (-5675552390126004252):::INT8), (e'\x00':::STRING, e'\x1d':::STRING, (-5353909169020148120):::INT8)), PARTITION table74_part_4 VALUES IN ((e'8t\x14\x13':::STRING, e'\x00':::STRING, (-2076855166914933686):::INT8), (e'r\x07nc q':::STRING, e'\x11':::STRING, 1899570840361400656:::INT8)), PARTITION table74_part_5 VALUES IN ((e'\x1b':::STRING, 'J':::STRING, (-3228451624343019173):::INT8), (e'\x17Z\ty\x16Uyj{':::STRING, e'\x19':::STRING, (-4116376490675854141):::INT8)), PARTITION table74_part_6 VALUES IN (('X':::STRING, '2':::STRING, (-5865707888760715052):::INT8), (e'\x17\x05\x1fcTU':::STRING, 'p':::STRING, 417701144915150808:::INT8)), PARTITION table74_part_7 VALUES IN ((e'8\x04&Y\\.\x11':::STRING, e'\r':::STRING, 127:::INT8), (e'+y\x14\x18':::STRING, e'\x00':::STRING, 3717268026797901550:::INT8)), PARTITION table74_part_8 VALUES IN (('':::STRING, '@':::STRING, (-3952916644766049872):::INT8), ('':::STRING, 'I':::STRING, 2783054515474739358:::INT8))), UNIQUE (col74_8) STORING (col74_0, col74_1, col74_2, col74_7), UNIQUE (col74_3 ASC, col74_1), UNIQUE (col74_6) STORING (col74_2, col74_8), INDEX (col74_9 ASC), FAMILY (col74_7, col74_3, col74_0, col74_1, col74_5), FAMILY (col74_4, col74_8, col74_2, col74_6))
        found first output
        "CREATE TABLE public.table74 (col74_0 BPCHAR NOT NULL, col74_1 STRING NULL, col74_2 INT8 NOT NULL, col74_3 INT8 NOT NULL, col74_4 INTERVAL NOT NULL, col74_5 INT4 NOT NULL, col74_6 BOX2D NOT NULL, col74_7 INT4 NOT NULL AS (abs(col74_5)) STORED, col74_8 INT8 NOT NULL AS (abs(col74_3)) STORED, col74_9 INT8 NOT NULL AS ((col74_3 + col74_2) + col74_5) VIRTUAL, col74_10 INT8 NOT NULL AS (col74_2 + col74_5) VIRTUAL, col74_11 STRING NOT NULL AS (lower(CAST(col74_6 AS STRING))) VIRTUAL, col74_12 INT8 NOT NULL AS (abs(col74_3)) VIRTUAL, CONSTRAINT table74_pkey PRIMARY KEY (col74_10 ASC, col74_6 ASC, col74_4 DESC), CONSTRAINT table74_col74_9_col74_0_col74_12_col74_1_col74_4_col74_6_col74_7_col74_11_key UNIQUE (col74_9 ASC, col74_0 DESC, col74_12 ASC, col74_1 DESC, col74_4 ASC, col74_6 ASC, col74_7 DESC, col74_11 ASC), INDEX table74_col74_8_col74_2_col74_0_col74_1_col74_7_col74_4_col74_3_col74_5_col74_12_col74_10_idx (col74_8 ASC, col74_2 ASC, col74_0 ASC, col74_1 DESC, col74_7 DESC, col74_4 ASC, col74_3 ASC, col74_5 ASC, col74_12 DESC, col74_10 DESC), CONSTRAINT table74_col74_3_key UNIQUE (col74_3 ASC), CONSTRAINT table74_col74_11_col74_0_col74_2_key UNIQUE (col74_11 DESC, col74_0 ASC, col74_2 ASC) PARTITION BY LIST (col74_11, col74_0, col74_2) (PARTITION table74_part_0 VALUES IN ((e'(\\x0e\\n]', ' ', 719093526511692457), (e'\\x11\\x19Q#7]', '(', 5274592778260151416)), PARTITION table74_part_1 VALUES IN ((e'4U_f>\\x7f\\x03+', e'\\r', 2208581895336924722), ('jV@_', e'\\x02', -2812879838062368897)), PARTITION table74_part_2 VALUES IN ((e'\\x11\\x06N\\x14\\x11', 'u', 2370269809838248347), (e'\\x1e\"', '3', 127)), PARTITION table74_part_3 VALUES IN ((e'\\x0eW\\x0eG88\\'\\x05\\x1f', 'Y', -5675552390126004252), (e'\\x00', e'\\x1d', -5353909169020148120)), PARTITION table74_part_4 VALUES IN ((e'8t\\x14\\x13', e'\\x00', -2076855166914933686), (e'r\\x07nc q', e'\\x11', 1899570840361400656)), PARTITION table74_part_5 VALUES IN ((e'\\x1b', 'J', -3228451624343019173), (e'\\x17Z\\ty\\x16Uyj{', e'\\x19', -4116376490675854141)), PARTITION table74_part_6 VALUES IN (('X', '2', -5865707888760715052), (e'\\x17\\x05\\x1fcTU', 'p', 417701144915150808)), PARTITION table74_part_7 VALUES IN ((e'8\\x04&Y\\\\.\\x11', e'\\r', 127), (e'+y\\x14\\x18', e'\\x00', 3717268026797901550)), PARTITION table74_part_8 VALUES IN (('', '@', -3952916644766049872), ('', 'I', 2783054515474739358))), CONSTRAINT table74_col74_8_key UNIQUE (col74_8 ASC) STORING (col74_0, col74_1, col74_2, col74_7), CONSTRAINT table74_col74_3_col74_1_key UNIQUE (col74_3 ASC, col74_1 ASC), CONSTRAINT table74_col74_6_key UNIQUE (col74_6 ASC) STORING (col74_2, col74_8), INDEX table74_col74_9_idx (col74_9 ASC), FAMILY fam_0_col74_7_col74_3_col74_0_col74_1_col74_5 (col74_7, col74_3, col74_0, col74_1, col74_5), FAMILY fam_1_col74_4_col74_8_col74_2_col74_6 (col74_4, col74_8, col74_2, col74_6))"
        but second output
        "CREATE TABLE public.table74 (col74_0 BPCHAR NOT NULL, col74_1 STRING NULL, col74_2 INT8 NOT NULL, col74_3 INT8 NOT NULL, col74_4 INTERVAL NOT NULL, col74_5 INT4 NOT NULL, col74_6 BOX2D NOT NULL, col74_7 INT4 NOT NULL AS (abs(col74_5)) STORED, col74_8 INT8 NOT NULL AS (abs(col74_3)) STORED, col74_9 INT8 NOT NULL AS ((col74_3 + col74_2) + col74_5) VIRTUAL, col74_10 INT8 NOT NULL AS (col74_2 + col74_5) VIRTUAL, col74_11 STRING NOT NULL AS (lower(CAST(col74_6 AS STRING))) VIRTUAL, col74_12 INT8 NOT NULL AS (abs(col74_3)) VIRTUAL, CONSTRAINT table74_pkey PRIMARY KEY (col74_10 ASC, col74_6 ASC, col74_4 DESC), CONSTRAINT table74_col74_9_col74_0_col74_12_col74_1_col74_4_col74_6_col74_7_col74_11_key UNIQUE (col74_9 ASC, col74_0 DESC, col74_12 ASC, col74_1 DESC, col74_4 ASC, col74_6 ASC, col74_7 DESC, col74_11 ASC), INDEX table74_col74_8_col74_2_col74_0_col74_1_col74_7_col74_4_col74_3_col74_5_col74_12_col74_10_idx (col74_8 ASC, col74_2 ASC, col74_0 ASC, col74_1 DESC, col74_7 DESC, col74_4 ASC, col74_3 ASC, col74_5 ASC, col74_12 DESC, col74_10 DESC), CONSTRAINT table74_col74_3_key UNIQUE (col74_3 ASC), CONSTRAINT table74_col74_11_col74_0_col74_2_key UNIQUE (col74_11 DESC, col74_0 ASC, col74_2 ASC) PARTITION BY LIST (col74_11, col74_0, col74_2) (PARTITION table74_part_0 VALUES IN ((e'(\\x0e\\n]', '', 719093526511692457), (e'\\x11\\x19Q#7]', '(', 5274592778260151416)), PARTITION table74_part_1 VALUES IN ((e'4U_f>\\x7f\\x03+', e'\\r', 2208581895336924722), ('jV@_', e'\\x02', -2812879838062368897)), PARTITION table74_part_2 VALUES IN ((e'\\x11\\x06N\\x14\\x11', 'u', 2370269809838248347), (e'\\x1e\"', '3', 127)), PARTITION table74_part_3 VALUES IN ((e'\\x0eW\\x0eG88\\'\\x05\\x1f', 'Y', -5675552390126004252), (e'\\x00', e'\\x1d', -5353909169020148120)), PARTITION table74_part_4 VALUES IN ((e'8t\\x14\\x13', e'\\x00', -2076855166914933686), (e'r\\x07nc q', e'\\x11', 1899570840361400656)), PARTITION table74_part_5 VALUES IN ((e'\\x1b', 'J', -3228451624343019173), (e'\\x17Z\\ty\\x16Uyj{', e'\\x19', -4116376490675854141)), PARTITION table74_part_6 VALUES IN (('X', '2', -5865707888760715052), (e'\\x17\\x05\\x1fcTU', 'p', 417701144915150808)), PARTITION table74_part_7 VALUES IN ((e'8\\x04&Y\\\\.\\x11', e'\\r', 127), (e'+y\\x14\\x18', e'\\x00', 3717268026797901550)), PARTITION table74_part_8 VALUES IN (('', '@', -3952916644766049872), ('', 'I', 2783054515474739358))), CONSTRAINT table74_col74_8_key UNIQUE (col74_8 ASC) STORING (col74_0, col74_1, col74_2, col74_7), CONSTRAINT table74_col74_3_col74_1_key UNIQUE (col74_3 ASC, col74_1 ASC), CONSTRAINT table74_col74_6_key UNIQUE (col74_6 ASC) STORING (col74_2, col74_8), INDEX table74_col74_9_idx (col74_9 ASC), FAMILY fam_0_col74_7_col74_3_col74_0_col74_1_col74_5 (col74_7, col74_3, col74_0, col74_1, col74_5), FAMILY fam_1_col74_4_col74_8_col74_2_col74_6 (col74_4, col74_8, col74_2, col74_6))"
    panic.go:626: -- test log scope end --
test logs left over in: outputs.zip/logTestCreateRandomSchema477618548
--- FAIL: TestCreateRandomSchema (4.98s)
```

Parameters:
 - <code>attempt=1</code>
 - <code>run=1</code>
 - <code>shard=6</code>
<details><summary>Help</summary>
<p>

See also: [How To Investigate a Go Test Failure \(internal\)](https://cockroachlabs.atlassian.net/l/c/HgfXfJgM)
</p>
</details>
<sub>

[This test on roachdash](https://roachdash.crdb.dev/?filter=status:open%20t:.*TestCreateRandomSchema.*&sort=title+created&display=lastcommented+project) | [Improve this report!](https://github.com/cockroachdb/cockroach/tree/master/pkg/cmd/bazci/githubpost/issues)

</sub>


Jira issue: CRDB-44209
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `108ce0f99414e4a76f5fa3e460706e6236e02f08` and the full history behind it is present.
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
