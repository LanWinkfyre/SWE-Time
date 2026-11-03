# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ui: ./dev gen js produces error and `crdb-api-client` is not buildable

Running `gen js` hits an error in `ui.go` that appears to be produced when copying files around.
```
❯ ./dev gen js
$ bazel build //pkg/ui/workspaces/eslint-plugin-crdb:eslint-plugin-crdb-lib //pkg/ui/workspaces/db-console/src/js:crdb-protobuf-client //pkg/ui/workspaces/cluster-ui:ts_project
INFO: Invocation ID: 5df9486d-ebc1-40ae-a385-5f72fe0dcf98
INFO: Analyzed 3 targets (0 packages loaded, 0 targets configured).
INFO: Found 3 targets...
INFO: Elapsed time: 1.885s, Critical Path: 0.64s
INFO: 4 processes: 3 remote cache hit, 1 internal.
INFO: Build completed successfully, 4 total actions
ERROR: Rel: can't make  relative to /private/var/tmp/_bazel_davidh/d61affdd093572eb0c41c4220c20a747/execroot/com_github_cockroachdb_cockroach/bazel-out/darwin_arm64-fastbuild/bin/pkg/ui/workspaces/eslint-plugin-crdb/dist
```

It has also been producing this error (known issue with `crdb-api-client` not being buildable)
```
INFO: Analyzed target //pkg/ui/workspaces/crdb-api-client:crdb-api-client (0 packages loaded, 36 targets configured).
ERROR: /Users/xinhao/go/src/github.com/cockroachdb/cockroach/pkg/ui/workspaces/crdb-api-client/BUILD.bazel:11:8: output 'pkg/ui/workspaces/crdb-api-client/dist' of //pkg/ui/workspaces/crdb-api-client:protos is a directory but was not declared as such
ERROR: /Users/xinhao/go/src/github.com/cockroachdb/cockroach/pkg/ui/workspaces/crdb-api-client/BUILD.bazel:11:8: Executing genrule //pkg/ui/workspaces/crdb-api-client:protos failed: not all outputs were created or valid
```

Jira issue: CRDB-41507

Epic CRDB-37557
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `cea63881b16ab19260a590e2dbf4f405881bd70e` and the full history behind it is present.
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
