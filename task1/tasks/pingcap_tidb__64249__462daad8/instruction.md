# Locate the commit that introduced this regression

A regression was reported against `pingcap/tidb`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
The rlike function encountered a problem with information_schema.

## Bug Report

Please answer these questions before submitting your issue. Thanks!

### 1. Minimal reproduce step (Required)

```
select version();
create database test_db_080;
create database test_db_081;
create database test_db_087;
select * from information_schema.schemata where schema_name like 'test_db_0%';
select * from information_schema.schemata where schema_name rlike 'test_db_0[0-8][0-7]';
```
<!-- a step by step guide for reproducing the bug. -->



After investigating, I see it's due to this PR.



### 2. What did you expect to see? (Required)


```
mysql> select version();
+--------------------+
| version()          |
+--------------------+
| 8.0.11-TiDB-v8.3.0 |
+--------------------+
1 row in set (0.00 sec)

mysql> create database test_db_080;
Query OK, 0 rows affected (0.03 sec)

mysql> create database test_db_081;
Query OK, 0 rows affected (0.03 sec)

mysql> create database test_db_087;
Query OK, 0 rows affected (0.03 sec)

mysql> select * from information_schema.schemata where schema_name like 'test_db_0%';
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
| CATALOG_NAME | SCHEMA_NAME | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH | TIDB_PLACEMENT_POLICY_NAME |
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
| def          | test_db_080 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
| def          | test_db_081 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
| def          | test_db_087 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
3 rows in set (0.00 sec)

mysql> select * from information_schema.schemata where schema_name rlike 'test_db_0[0-8][0-7]';
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
| CATALOG_NAME | SCHEMA_NAME | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH | TIDB_PLACEMENT_POLICY_NAME |
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
| def          | test_db_080 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
| def          | test_db_081 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
| def          | test_db_087 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
```

### 3. What did you see instead (Required)

```
mysql> select version();
+--------------------+
| version()          |
+--------------------+
| 8.0.11-TiDB-v8.5.0 |
+--------------------+
1 row in set (0.00 sec)

mysql> create database test_db_080;
Query OK, 0 rows affected (0.05 sec)

mysql> create database test_db_081;
Query OK, 0 rows affected (0.04 sec)

mysql> create database test_db_087;
Query OK, 0 rows affected (0.03 sec)

mysql> select * from information_schema.schemata where schema_name like 'test_db_0%';
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
| CATALOG_NAME | SCHEMA_NAME | DEFAULT_CHARACTER_SET_NAME | DEFAULT_COLLATION_NAME | SQL_PATH | TIDB_PLACEMENT_POLICY_NAME |
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
| def          | test_db_080 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
| def          | test_db_081 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
| def          | test_db_087 | utf8mb4                    | utf8mb4_bin            | NULL     | NULL                       |
+--------------+-------------+----------------------------+------------------------+----------+----------------------------+
3 rows in set (0.00 sec)

mysql> select * from information_schema.schemata where schema_name rlike 'test_db_0[0-8][0-7]';
Empty set (0.00 sec)

```

### 4. What is your TiDB version? (Required)
TiDB-v8.5.0 ~ TiDB-v8.5.3
<!-- Paste the output of SELECT tidb_version() -->
```

## What you have

- `/testbed/repo` is a git clone of `pingcap/tidb` truncated just after the regression was
  reported.  `HEAD` is `bce559b421ad7436c05f61f6222e11cb6c01adbe` and the full history behind it is present.
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
