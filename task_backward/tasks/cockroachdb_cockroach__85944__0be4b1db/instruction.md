# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
serverccl: package times out during shutdown causing flakes

**Describe the problem**

The serverccl package has been timing out.
- [here](https://teamcity.cockroachdb.com/buildConfiguration/Cockroach_UnitTests_BazelUnitTests/6029962?buildTab=overview&showRootCauses=false&expandBuildProblemsSection=true&expandBuildTestsSection=true&expandBuildChangesSection=true&expandBuildDeploymentsSection=true#%2Ftmp%2F_tmp%2Fc101b7a464a1afc1f5af0cd85792187e%2FlogTestNoInflightTracesVirtualTableOnTenant2070669194;%2Ftmp%2F_tmp%2Fc101b7a464a1afc1f5af0cd85792187e%2FStartServer2953751379;%2Fbazel-testlogs%2Fpkg%2Fccl%2Fserverccl%2Fserverccl_test;%2Fbazel-testlogs%2Fpkg%2Fccl%2Fserverccl%2Fstatusccl;%2Fbazel-testlogs%2Fpkg%2Fccl%2Fserverccl%2Fdiagnosticsccl) ([logs](https://teamcityartifacts.crdb.io/presignedTokenAuth/cbf22e43-ce1e-4d2d-bc2e-c1d977b8872b/repository/download/Cockroach_UnitTests_BazelUnitTests/6029962:id/bazel-testlogs/pkg/ccl/serverccl/serverccl_test/test.log))
- [here](https://teamcityartifacts.crdb.io/presignedTokenAuth/eefa002d-e9f4-494c-81e1-a8968242aae7/repository/download/Cockroach_UnitTests_BazelUnitTests/6033094:id/bazel-testlogs/pkg/ccl/serverccl/serverccl_test/test.log)
- [here](https://teamcity.cockroachdb.com/viewLog.html?buildId=6040534&problemId=4141)
- [here](https://teamcity.cockroachdb.com/buildConfiguration/Cockroach_UnitTests/6046487?showRootCauses=false&expandBuildChangesSection=true&expandBuildProblemsSection=true&expandBuildTestsSection=true)

One theory:
> Seems like the server fails to shut down because we’re waiting for quiescence but the contexts are not getting canceled correctly or something and we’re in an infinite retry inside `kv/kvclient/rangecache.(*RangeCache).tryLookup`.



**To Reproduce**

The TestNoInflightTracesVirtualTableOnTenant test reproes it.

```
./dev test pkg/ccl/serverccl --stress --filter=TestNoInflightTracesVirtualTableOnTenant --timeout=2m --test-args='-test.timeout 20s'
```


Jira issue: CRDB-18494
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `43bfc3185cb362b14e0b8a331148f0b14542a4f2` and the full history behind it is present.
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
