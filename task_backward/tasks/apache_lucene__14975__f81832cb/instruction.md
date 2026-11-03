# Locate the commit that introduced this regression

A regression was reported against `apache/lucene`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TestParentsChildrenBlockJoinQuery.testAdvance failure

### Description

The test is failing with the following assertion error:

```
   >     java.lang.AssertionError: expected:<3> but was:<4>
   >         at __randomizedtesting.SeedInfo.seed([6FFB2750FC36CC8E:F3013CCA5598320D]:0)
   >         at junit@4.13.2/org.junit.Assert.fail(Assert.java:89)
   >         at junit@4.13.2/org.junit.Assert.failNotEquals(Assert.java:835)
   >         at junit@4.13.2/org.junit.Assert.assertEquals(Assert.java:647)
   >         at junit@4.13.2/org.junit.Assert.assertEquals(Assert.java:633)
   >         at org.apache.lucene.search.join.TestParentsChildrenBlockJoinQuery.testAdvance(TestParentsChildrenBlockJoinQuery.java:211)
   >         at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:104)
   >         at java.base/java.lang.reflect.Method.invoke(Method.java:565)

```

git bisect points to this commit:



### Gradle command to reproduce

./gradlew test --tests TestParentsChildrenBlockJoinQuery.testAdvance -Dtests.seed=6FFB2750FC36CC8E
```

## What you have

- `/testbed/repo` is a git clone of `apache/lucene` truncated just after the regression was
  reported.  `HEAD` is `346d7624db510c3bc2cb9012f6a01f29d98ac5de` and the full history behind it is present.
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
