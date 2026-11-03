# Locate the commit that introduced this regression

A regression was reported against `apache/lucene`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Reproducible test failure in TestLucene90FieldInfosFormat.testRandom

### Description




```
org.apache.lucene.codecs.lucene90.TestLucene90FieldInfosFormat > testRandom FAILED
    java.lang.IllegalArgumentException: parent document and soft-deletes field can't be the same field ""
        at __randomizedtesting.SeedInfo.seed([E9414A90E55BE2D:7CD831A6BF35085E]:0)
        at org.apache.lucene.index.FieldInfos$FieldNumbers.<init>(FieldInfos.java:402)
        at org.apache.lucene.index.IndexWriter$5$1.<init>(IndexWriter.java:6626)
        at org.apache.lucene.index.IndexWriter$5.newFieldInfosBuilder(IndexWriter.java:6625)
        at org.apache.lucene.tests.index.BaseFieldInfoFormatTestCase.testRandom(BaseFieldInfoFormatTestCase.java:281)
        at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
```

```
./gradlew test --tests TestLucene90FieldInfosFormat.testRandom -Dtests.seed=E9414A90E55BE2D -Dtests.nightly=true -Dtests.locale=da -Dtests.timezone=Japan -Dtests.asserts=true -Dtests.file.encoding=UTF-8
```




### Gradle command to reproduce

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `apache/lucene` truncated just after the regression was
  reported.  `HEAD` is `8f759d5bf65079f8841224547b2b10b4c5f51f76` and the full history behind it is present.
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
