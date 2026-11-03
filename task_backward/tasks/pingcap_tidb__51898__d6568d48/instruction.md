# Locate the commit that introduced this regression

A regression was reported against `pingcap/tidb`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
There is a 2%-4% performance regression in sysbench select_random_points

## Bug Report

Please answer these questions before submitting your issue. Thanks!

### 1. Minimal reproduce step (Required)
1. deploy a tidb cluster 
2. run sysbench select_random_points

<!-- a step by step guide for reproducing the bug. -->

### 2. What did you expect to see? (Required)
No performance regression
### 3. What did you see instead (Required)

![image](https://github.com/pingcap/tidb/assets/84501897/209fe97c-7db3-445b-bc1e-07c8f3566e5c)


![image](https://github.com/pingcap/tidb/assets/84501897/4c34bf67-5051-4e24-bc09-997847aafcf9)

### 4. What is your TiDB version? (Required)

<!-- Paste the output of SELECT tidb_version() -->



<img width="855" alt="截屏2024-03-20 11 27 32" src="https://github.com/pingcap/tidb/assets/9039012/1c940c96-1e48-4b75-9b5e-38e3a8b67fff">

In the new CPU profile, we can see that there is additional CPU overhead in the index usage reporter section.
```

## What you have

- `/testbed/repo` is a git clone of `pingcap/tidb` truncated just after the regression was
  reported.  `HEAD` is `61c471487ef73f21ee453fe6ad18aaf9070d44cd` and the full history behind it is present.
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
