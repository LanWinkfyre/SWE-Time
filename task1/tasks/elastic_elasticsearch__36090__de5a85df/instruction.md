# Locate the commit that introduced this regression

A regression was reported against `elastic/elasticsearch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression in multi-level string bucket terms aggregation from 5 to 6 crashes Elasticsearch with OOM

**Elasticsearch version** (`bin/elasticsearch --version`): Various between 5, 6 and master, see description

**Plugins installed**: default zip-package or built from source without modification, no other plugins installed

**JVM version** (`java -version`): mostly 1.8.0_161, newer Java when required for newer Versions of Elasticsearch

**OS version** (`uname -a` if on a Unix-like system): Windows 10, Linux 4.14.62-65.117.amzn1.x86_64 #1 SMP Fri Aug 10 20:03:52 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

**Description of the problem including expected versus actual behavior**:

We are in the process of upgrading our large rollout of Elasticsearch from version 5 to 6. 

We encountered a query where Elasticsearch 5 is able to handle a multi-level string bucket terms query just fine, whereas Elasticsearch 6 quickly crashes with Java out of memory exceptions, even when providing twice as much memory to the process. 

It seems there is a regression in memory usage in the newer version of Elasticsearch. Initial analysis indicates that the switch to Lucene 7 (done as part of 6.0), introduced this.

With default -Xmx1g and documents with 4 fields with 5, 1250, 12423 and 62467 unique values each cause Elasticsearch 6 to quickly crash with out of memory when executing the following query:

```
{
  "size": 0,
  "aggregations": {
    "q0": {
      "terms": {
        "field": "level1",
        "size": 10
      },
      "aggregations": {
        "q0": {
          "terms": {
            "field": "level2",
            "size": 200
          },
          "aggregations": {
            "q0": {
              "terms": {
                "field": "level3",
                "size": 100
              },
              "aggregations": {
                "q0": {
                  "terms": {
                    "field": "level4",
                    "size": 1000
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

**Steps to reproduce**:

[StringTermsOOMIT.zip](https://github.com/elastic/elasticsearch/files/2631184/StringTermsOOMIT.zip)

The attached zip-file contains a Java integration-test-case which triggers the problem. You can run it via the following command:

`gradle -Dtests.heap.size=500m --no-daemon :core:integTest "-Dtests.class=*.StringTermsOOMIT"`

The "-Xmx500m" is used to speed up test execution. With the default 1g the same can be triggered by using higher-cardinality fields and more documents, which causes the test to run much longer.

The fact that Elasticsearch simply crashes with an OOM is bad, as this makes it impossible to run this version in a production setting whenever you want to allow fairly complex queries to be executed.

Note: on current master, some bucket-limit-check kicks in now, so it seems at least some "harakiri-prevention" was put in place there, but the increased memory usage is still present and queries that could easily be executed before are not possible any more.

**Root cause**:

I ran a `git bisect` using this test to identify the commit which caused this, it resulted in the following:








**Affected versions/branches**:

We ran a suite of test-runs on various versions, we see the following behavior of the respective Git branches/tags:

5.0 -> Ok
v5.3.3 -> Ok
v5.6.5 -> Ok

v6.0.0-alpha1 -> OOM
v6.2.4 -> OOM
v6.4.2 -> OOM
v6.5.1 -> OOM
6.4 -> OOM
6.5 -> OOM
6.x -> OOM
master -> query fails due to new default bucket-limit of 10k, when this limit is removed, it still goes OOM

The attached zip contains output from runs against branches 5.0, 6.x and master

[StringTermsOOMIT.zip](https://github.com/elastic/elasticsearch/files/2631184/StringTermsOOMIT.zip)
```

## What you have

- `/testbed/repo` is a git clone of `elastic/elasticsearch` truncated just after the regression was
  reported.  `HEAD` is `78e07d467c87e4728734b0da1ebc50f43109175e` and the full history behind it is present.
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
