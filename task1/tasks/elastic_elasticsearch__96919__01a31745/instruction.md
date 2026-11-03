# Locate the commit that introduced this regression

A regression was reported against `elastic/elasticsearch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
org.elasticsearch.health.node.DiskHealthIndicatorServiceIT.testRed failed on main

### CI Link

https://gradle-enterprise.elastic.co/s/g5lnen3vqybaa

### Repro line

./gradlew ':server:internalClusterTest' --tests "org.elasticsearch.health.node.DiskHealthIndicatorServiceIT.testRed" \   -Dtests.seed=BFEB6603081AAC8A \   -Dtests.locale=lv \   -Dtests.timezone=America/Cancun \   -Druntime.java=20

### Does it reproduce?

Yes

### Applicable branches

main

### Failure history

_No response_

### Failure excerpt

10:13:46 REPRODUCE WITH: ./gradlew ':server:internalClusterTest' --tests "org.elasticsearch.health.node.DiskHealthIndicatorServiceIT.testRed" -Dtests.seed=BFEB6603081AAC8A -Dtests.locale=lv -Dtests.timezone=America/Cancun -Druntime.java=20
10:13:46 
10:13:46 org.elasticsearch.health.node.DiskHealthIndicatorServiceIT > testRed FAILED
10:13:46     java.lang.AssertionError: 
10:13:46     Expected: <RED>
10:13:46          but: was <GREEN>
10:13:46         at __randomizedtesting.SeedInfo.seed([BFEB6603081AAC8A:955469E053FFD5D6]:0)
10:13:46         at org.hamcrest.MatcherAssert.assertThat(MatcherAssert.java:18)
10:13:46         at org.junit.Assert.assertThat(Assert.java:956)
10:13:46         at org.junit.Assert.assertThat(Assert.java:923)
10:13:46         at org.elasticsearch.health.node.DiskHealthIndicatorServiceIT.testRed(DiskHealthIndicatorServiceIT.java:62)


 Assigning to myseld
```

## What you have

- `/testbed/repo` is a git clone of `elastic/elasticsearch` truncated just after the regression was
  reported.  `HEAD` is `97fd810757fd28ef1eb82776cf4c97ef894e8ad9` and the full history behind it is present.
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
