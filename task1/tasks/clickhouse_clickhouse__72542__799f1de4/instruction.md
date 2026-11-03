# Locate the commit that introduced this regression

A regression was reported against `ClickHouse/ClickHouse`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Raft communication issue between Keeper versions 24.8 and 24.9

**Describe what's wrong**

When doing a rolling upgrade from 24.8.5.115 to 24.9.x (or higher) in a cluster of 3 Clickhouse Keeper instances, the first node to be upgraded to the new version (24.9.x) fails to rejoin the cluster, while logging errors about Raft CRC mismatches and "wrong version number (SSL routines)". See the error logs at the end of this issue. 

We were able to reproduce this with all combinations of these versions:
- v24.9.1.3278-stable, v24.9.2.42-stable, v24.9.3.128-stable, v24.10.3.21-stable, 24.11.1.2557 for the node that gets upgraded ("new version") 
- v24.8.5.115-lts and v24.8.7.41-lts for the rest of the cluster ("old version")

The issue can be reproduced with this [simple docker setup](https://github.com/IngaFeick/clickhouse_issue). 

Raft config:
```xml
...
      <raft_configuration>
            <secure>true</secure>
            <server>
                <id>1</id>
                <hostname>clickhouse-keeper1</hostname>
                <port>9234</port>
            </server>
            <server>
                <id>2</id>
                <hostname>clickhouse-keeper2</hostname>
                <port>9234</port>
            </server>
            <server>
                <id>3</id>
                <hostname>clickhouse-keeper3</hostname>
                <port>9234</port>
            </server>
        </raft_configuration>
...
```
The full configuration can be found in the [demo project](https://github.com/IngaFeick/clickhouse_issue/blob/test_setup/configs/keeper_config1.xml).

**Does it reproduce on the most recent release?**

Yes, we also tested this for version 24.11.1.2557 (for the upgrading node, against a 24.8 cluster). 

**Expected behavior**

We'd expect not to see the Raft issues logged and for the upgraded node to join the keeper cluster. 

**Error message and/or stacktrace**

On the node that has the new version (`clickhouse-keeper3` in the test project):


On the other nodes with the old versions (`clickhouse-keeper1` and `clickhouse-keeper2` in the test project): 
```
2024.11.27 12:14:02.894655 [ 44 ] {} <Error> RaftInstance: session 459 handshake with ::ffff:172.23.0.16:42346 failed: error 167772427, wrong version number (SSL routines)
2024.11.27 12:14:02.975671 [ 53 ] {} <Error> RaftInstance: failed SSL handshake with peer 3, clickhouse-keeper3:9234, error 104, Connection reset by peer
```
```

## What you have

- `/testbed/repo` is a git clone of `ClickHouse/ClickHouse` truncated just after the regression was
  reported.  `HEAD` is `ec914b108ed8464ca24a7e8e5a1fcd775f39a2c6` and the full history behind it is present.
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
