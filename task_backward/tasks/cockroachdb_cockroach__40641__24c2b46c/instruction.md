# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
sql: vec: experimental_on has incorrect results

```
SELECT
	c_name,
	c_custkey,
	o_orderkey,
	o_orderdate,
	o_totalprice,
	sum(l_quantity)
FROM
	customer,
	orders,
	lineitem
WHERE
	o_orderkey IN (
		SELECT
			l_orderkey
		FROM
			lineitem
		GROUP BY
			l_orderkey HAVING
				sum(l_quantity) > 127
	)
	AND c_custkey = o_custkey
	AND o_orderkey = l_orderkey
GROUP BY
	c_name,
	c_custkey,
	o_orderkey,
	o_orderdate,
	o_totalprice
ORDER BY
	o_totalprice DESC,
	o_orderdate
LIMIT 1;
```

With the TPCH dataset loaded, the above query gives identical results in postgres, cockroach with vec=auto, and cockroach with vec=off. When vec=experimental_on, the output changes:

vec=auto:

```
       c_name       | c_custkey | o_orderkey | o_orderdate | o_totalprice | sum 
--------------------+-----------+------------+-------------+--------------+-----
 Customer#000058534 |     58534 |    4145926 | 1996-10-03  |  581111.3125 | 326

```

vec=experimental_on:

```
       c_name       | c_custkey | o_orderkey | o_orderdate | o_totalprice | sum 
--------------------+-----------+------------+-------------+--------------+-----
 Customer#000142196 |    142196 |    4442851 | 1992-01-24  | 459709.96875 | 249
```
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `a41355dabc985310e84ca32e890cd8318ff1f155` and the full history behind it is present.
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
