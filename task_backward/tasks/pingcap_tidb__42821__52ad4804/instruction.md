# Locate the commit that introduced this regression

A regression was reported against `pingcap/tidb`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
## Bug Report

Please answer these questions before submitting your issue. Thanks!

### 1. Minimal reproduce step (Required)

**Setup the environment:**

```
CREATE TABLE t4 (vkey int(11), c13 double);
INSERT INTO t4 VALUES (31,0);
CREATE TABLE t7 (vkey int(11), pkey int(11), c26 double, c27 int(11));
INSERT INTO t7 VALUES (29,164000,0,NULL);
```

**Testcase 1**
```
select 1 as c0
from
  (t7 as ref_0
    inner join (t7 as ref_1
      right join t4 as ref_2
      on (ref_1.vkey = ref_2.vkey ))
    on (ref_0.c26 = ref_2.c13 ))
where not (not (
             (nullif(ref_0.pkey, ref_1.c27) is not null) and false
          ));
```
Testcase 1 outputs 1 row.

```
+----+
| c0 |
+----+
|  1 |
+----+
1 row in set (0.00 sec)
```

Then, I replace `(nullif(ref_0.pkey, ref_1.c27) is not null) and false` with `false`. The results should not be changed because `anything and false` is `false`. The test case becomes:

**Testcase 2**
```
select 1 as c0
from
  (t7 as ref_0
    inner join (t7 as ref_1
      right join t4 as ref_2
      on (ref_1.vkey = ref_2.vkey ))
    on (ref_0.c26 = ref_2.c13 ))
where not (not (
             false
          ));
```

### 2. What did you expect to see? (Required)

Testcase 1 and Testcase 2 should output the same results.

### 3. What did you see instead (Required)

Testcase 2 outputs
```
Empty set (0.00 sec)
```
While Testcase 1 outputs:
```
+----+
| c0 |
+----+
|  1 |
+----+
1 row in set (0.00 sec)
```


### 4. What is your TiDB version? (Required)

+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Edition: Community

Git Branch: master
UTC Build Time: 2023-03-23 13:57:53
GoVersion: go1.20.2
Race Enabled: false
TiKV Min Version: 6.2.0-alpha
Check Table Before Drop: false
Store: unistore |
+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
```

## What you have

- `/testbed/repo` is a git clone of `pingcap/tidb` truncated just after the regression was
  reported.  `HEAD` is `a0f2405981960ec705bf44f12b96ca8aec1506c4` and the full history behind it is present.
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
