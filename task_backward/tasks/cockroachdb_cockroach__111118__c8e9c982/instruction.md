# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
opt/bench: regression in BenchmarkPhases/many-columns-and-indexes


```
name                                                     old time/op    new time/op    delta
Phases/many-columns-and-indexes-a/Simple/Explore-24         447µs ± 1%     488µs ± 0%    +9.20%  (p=0.000 n=9+8)
Phases/many-columns-and-indexes-a/Simple/ExecBuild-24       453µs ± 0%     497µs ± 0%    +9.63%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/Explore-24       388µs ± 0%     432µs ± 0%   +11.36%  (p=0.000 n=9+10)
Phases/many-columns-and-indexes-a/Prepared/ExecBuild-24     394µs ± 0%     439µs ± 0%   +11.28%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/Explore-24         532µs ± 0%     582µs ± 0%    +9.52%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/ExecBuild-24       543µs ± 1%     594µs ± 1%    +9.35%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Prepared/Explore-24       441µs ± 1%     492µs ± 0%   +11.44%  (p=0.000 n=10+9)
Phases/many-columns-and-indexes-b/Prepared/ExecBuild-24     449µs ± 0%     501µs ± 1%   +11.70%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Simple/Explore-24         346ms ± 1%     347ms ± 1%      ~     (p=0.203 n=10+8)
Phases/many-columns-and-indexes-c/Simple/ExecBuild-24       348ms ± 1%     345ms ± 2%      ~     (p=0.123 n=10+10)
Phases/many-columns-and-indexes-c/Prepared/Explore-24       333ms ± 2%     346ms ± 1%    +3.84%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Prepared/ExecBuild-24     336ms ± 0%     346ms ± 1%    +3.05%  (p=0.000 n=7+10)

name                                                     old alloc/op   new alloc/op   delta
Phases/many-columns-and-indexes-a/Simple/Explore-24        39.4kB ± 0%    53.0kB ± 0%   +34.48%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Simple/ExecBuild-24      40.2kB ± 0%    53.8kB ± 0%   +33.81%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/Explore-24      5.36kB ± 0%   18.81kB ± 0%  +250.92%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/ExecBuild-24    6.16kB ± 0%   19.61kB ± 0%  +218.43%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/Explore-24        47.7kB ± 0%    61.3kB ± 0%   +28.47%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/ExecBuild-24      48.8kB ± 0%    62.4kB ± 0%   +27.79%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Prepared/Explore-24      7.88kB ± 0%   21.33kB ± 0%  +170.77%  (p=0.000 n=8+10)
Phases/many-columns-and-indexes-b/Prepared/ExecBuild-24    9.01kB ± 0%   22.47kB ± 0%  +149.31%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Simple/Explore-24         110MB ± 0%     111MB ± 0%    +0.50%  (p=0.000 n=10+9)
Phases/many-columns-and-indexes-c/Simple/ExecBuild-24       110MB ± 0%     111MB ± 0%    +0.49%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Prepared/Explore-24       109MB ± 0%     109MB ± 0%    +0.49%  (p=0.000 n=9+10)
Phases/many-columns-and-indexes-c/Prepared/ExecBuild-24     109MB ± 0%     109MB ± 0%    +0.50%  (p=0.000 n=10+10)

name                                                     old allocs/op  new allocs/op  delta
Phases/many-columns-and-indexes-a/Simple/Explore-24          76.0 ± 0%     111.0 ± 0%   +46.05%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Simple/ExecBuild-24        87.0 ± 0%     122.0 ± 0%   +40.23%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/Explore-24        28.0 ± 0%      61.0 ± 0%  +117.86%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/ExecBuild-24      39.0 ± 0%      72.0 ± 0%   +84.62%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/Explore-24           131 ± 0%       166 ± 0%   +27.02%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/ExecBuild-24         146 ± 0%       181 ± 0%   +23.97%  (p=0.000 n=10+8)
Phases/many-columns-and-indexes-b/Prepared/Explore-24        46.0 ± 0%      79.0 ± 0%   +71.74%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Prepared/ExecBuild-24      61.0 ± 0%      94.0 ± 0%   +54.10%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Simple/Explore-24          750k ± 0%      763k ± 0%    +1.75%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Simple/ExecBuild-24        750k ± 0%      763k ± 0%    +1.75%  (p=0.000 n=8+10)
Phases/many-columns-and-indexes-c/Prepared/Explore-24        744k ± 0%      757k ± 0%    +1.76%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Prepared/ExecBuild-24      744k ± 0%      758k ± 0%    +1.76%  (p=0.000 n=10+10)
```
(comparison of the whole benchmark is [here](https://gist.github.com/yuzefovich/3b930facc2d1148f13d40e0ab2663c99)).


<details>
```

name                                                     old time/op    new time/op    delta
Phases/many-columns-and-indexes-a/Simple/Explore-24         436µs ± 0%     483µs ± 0%   +10.92%  (p=0.000 n=10+9)
Phases/many-columns-and-indexes-a/Simple/ExecBuild-24       445µs ± 2%     493µs ± 1%   +10.58%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/Explore-24       380µs ± 1%     425µs ± 0%   +11.69%  (p=0.000 n=10+8)
Phases/many-columns-and-indexes-a/Prepared/ExecBuild-24     384µs ± 0%     432µs ± 0%   +12.31%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/Explore-24         522µs ± 1%     576µs ± 0%   +10.43%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/ExecBuild-24       533µs ± 0%     588µs ± 1%   +10.39%  (p=0.000 n=9+10)
Phases/many-columns-and-indexes-b/Prepared/Explore-24       429µs ± 0%     482µs ± 0%   +12.20%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Prepared/ExecBuild-24     438µs ± 0%     490µs ± 1%   +11.90%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Simple/Explore-24         348ms ± 1%     347ms ± 1%      ~     (p=0.780 n=10+9)
Phases/many-columns-and-indexes-c/Simple/ExecBuild-24       349ms ± 1%     350ms ± 2%      ~     (p=0.739 n=10+10)
Phases/many-columns-and-indexes-c/Prepared/Explore-24       328ms ± 2%     330ms ± 2%      ~     (p=0.684 n=10+10)
Phases/many-columns-and-indexes-c/Prepared/ExecBuild-24     330ms ± 2%     326ms ± 0%      ~     (p=0.122 n=10+8)

name                                                     old alloc/op   new alloc/op   delta
Phases/many-columns-and-indexes-a/Simple/Explore-24        39.4kB ± 0%    52.8kB ± 0%   +34.02%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Simple/ExecBuild-24      40.2kB ± 0%    53.6kB ± 0%   +33.35%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/Explore-24      5.36kB ± 0%   18.75kB ± 0%  +249.84%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/ExecBuild-24    6.16kB ± 0%   19.55kB ± 0%  +217.52%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/Explore-24        47.7kB ± 0%    61.1kB ± 0%   +28.09%  (p=0.000 n=10+9)
Phases/many-columns-and-indexes-b/Simple/ExecBuild-24      48.8kB ± 0%    62.2kB ± 0%   +27.44%  (p=0.000 n=9+10)
Phases/many-columns-and-indexes-b/Prepared/Explore-24      7.88kB ± 0%   21.27kB ± 0%  +169.94%  (p=0.000 n=10+9)
Phases/many-columns-and-indexes-b/Prepared/ExecBuild-24    9.01kB ± 0%   22.41kB ± 0%  +148.58%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Simple/Explore-24         107MB ± 0%     107MB ± 0%    +0.14%  (p=0.000 n=10+9)
Phases/many-columns-and-indexes-c/Simple/ExecBuild-24       107MB ± 0%     108MB ± 0%    +0.14%  (p=0.000 n=9+10)
Phases/many-columns-and-indexes-c/Prepared/Explore-24       106MB ± 0%     106MB ± 0%    +0.14%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Prepared/ExecBuild-24     106MB ± 0%     106MB ± 0%    +0.14%  (p=0.000 n=10+10)

name                                                     old allocs/op  new allocs/op  delta
Phases/many-columns-and-indexes-a/Simple/Explore-24          76.0 ± 0%     109.0 ± 0%   +43.42%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Simple/ExecBuild-24        87.0 ± 0%     120.0 ± 0%   +37.93%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/Explore-24        28.0 ± 0%      61.0 ± 0%  +117.86%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-a/Prepared/ExecBuild-24      39.0 ± 0%      72.0 ± 0%   +84.62%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/Explore-24           131 ± 0%       164 ± 0%   +25.19%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Simple/ExecBuild-24         146 ± 0%       179 ± 0%   +22.60%  (p=0.000 n=10+8)
Phases/many-columns-and-indexes-b/Prepared/Explore-24        46.0 ± 0%      79.0 ± 0%   +71.74%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-b/Prepared/ExecBuild-24      61.0 ± 0%      94.0 ± 0%   +54.10%  (p=0.000 n=10+10)
Phases/many-columns-and-indexes-c/Simple/Explore-24          735k ± 0%      735k ± 0%    +0.05%  (p=0.000 n=10+9)
Phases/many-columns-and-indexes-c/Simple/ExecBuild-24        735k ± 0%      735k ± 0%    +0.05%  (p=0.000 n=9+10)
Phases/many-columns-and-indexes-c/Prepared/Explore-24        729k ± 0%      729k ± 0%    +0.05%  (p=0.000 n=10+8)
Phases/many-columns-and-indexes-c/Prepared/ExecBuild-24      729k ± 0%      729k ± 0%    +0.05%  (p=0.000 n=10+10)
```

</details>

Jira issue: CRDB-31774
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `e9a8c49a495178fa1160cc50b1e89c802816e0c7` and the full history behind it is present.
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
