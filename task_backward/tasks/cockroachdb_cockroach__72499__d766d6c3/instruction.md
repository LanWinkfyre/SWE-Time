# Locate the commit that introduced this regression

A regression was reported against `cockroachdb/cockroach`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
roachperf: `kv95` and `kv0` regression around October 28th

Some versions of `kv95` and `kv0` saw a ~10% performance regression around October 28th, e.g. `kv95/enc=false/nodes=1/cpu=32`:

<a href="https://roachperf.crdb.dev/?filter=&view=kv95%2Fenc%3Dfalse%2Fnodes%3D1%2Fcpu%3D32&tab=gce"><img width="847" alt="Screenshot 2021-11-06 at 14 25 52" src="https://user-images.githubusercontent.com/644420/140611333-9b2a68b8-fd8e-41bd-8b93-bb0693f4ff2f.png"></a>

This is even more pronounced with 64KB payloads, e.g. `kv95/enc=false/nodes=3/cpu=32/size=64kb`:

<a href="https://roachperf.crdb.dev/?filter=&view=kv95%2Fenc%3Dfalse%2Fnodes%3D3%2Fcpu%3D32%2Fsize%3D64kb&tab=gce"><img width="846" alt="Screenshot 2021-11-06 at 14 29 17" src="https://user-images.githubusercontent.com/644420/140611457-78abf2fb-8013-4bcd-b165-3c7ea2d71514.png"></a>

 Running a couple of benchmarks to confirm.

cc @sumeerbhola 

The regression should only be for cases where the LSM was degrading prior to admission control (admission control is not expected to reduce throughput if the bottleneck was CPU). If one clicks to get details of a run, and sees something like the following where the rate fluctuates, it is because for LSM overload the tokens get adjusted every 15s (unhealthy for 15s, so fewer tokens, resulting in transition to healthy, with unconstrained tokens, and then repeat). Admission control will only affect writes in this case but since we are issuing a sequence of reads and writes from the same workers, reducing write throughput also reduces read throughput.

<img width="980" alt="Screen Shot 2021-11-10 at 11 15 43 AM" src="https://user-images.githubusercontent.com/54990988/141150746-c111b99d-baf2-4c20-b83c-29a9da7053c5.png">

The corresponding no-admission roachtest has a higher mean rate, but note the decline in rate over time as the LSM becomes more and more unhealthy. It is not a sustainable rate, but since we only run for 10min we have overlooked this problem.

<img width="971" alt="Screen Shot 2021-11-10 at 11 20 05 AM" src="https://user-images.githubusercontent.com/54990988/141151593-47088fdb-3fa1-4289-81bc-64f18d5258bc.png">

You should see the same thing with the kv0 slowdowns.

But this is not the case with `kv95/enc=false/nodes=1/cpu=32`, and kv95 typically needs to have larger block sizes to cause write overload, which makes me suspicious that it could be a different root cause. We didn't have an "admission" variant for this test prior to the enabling of admission control, but we did have it for `kv95/enc=false/nodes=3/cpu=32`. See the screenshots below for the with and without admission for a randomly picked day (Oct 17) -- they are close:

<img width="952" alt="Screen Shot 2021-11-10 at 11 27 53 AM" src="https://user-images.githubusercontent.com/54990988/141152780-96c731f0-462d-4ede-8163-49fb9142db77.png">
<img width="945" alt="Screen Shot 2021-11-10 at 11 29 03 AM" src="https://user-images.githubusercontent.com/54990988/141152920-f96da116-9046-4271-b647-15a961bc8630.png">



>The corresponding no-admission roachtest has a higher mean rate, but note the decline in rate over time as the LSM becomes more and more unhealthy. It is not a sustainable rate, but since we only run for 10min we have overlooked this problem.

Interesting find. This seems fine then, since presumably running for another 10 minutes could have shown an overall improvement when admission control is enabled.

> But this is not the case with `kv95/enc=false/nodes=1/cpu=32`, and kv95 typically needs to have larger block sizes to cause write overload, which makes me suspicious that it could be a different root cause.

Interesting, I'll run another bisection and see if something turns up. Thanks!

In light of this, should we consider running these perf tests for longer than ten minutes (say thirty minutes)? This will completely shift the graphs we see (since they use total qps or something like that) but it may give us better data in the long run?

Yeah, 30 minutes makes sense. That probably shouldn't be the default though, since people will run these from the command-line as well, but for the nightlies that seems reasonable.

I'll submit a PR.

> Yeah, 30 minutes makes sense. That probably shouldn't be the default though, since people will run these from the command-line as well, but for the nightlies that seems reasonable. I'll submit a PR.

Thanks! You don't think that approach will be confusing to people trying to repro the numbers? I would've thought 30m is the default but it should be "easy" to lower that to 10 minutes when desired, perhaps through an env var (I know you love those!) or small code change (but code change sucks for bisecting).
```

## What you have

- `/testbed/repo` is a git clone of `cockroachdb/cockroach` truncated just after the regression was
  reported.  `HEAD` is `46b7efa32c57b15f4ae6e0d75845f63360b62161` and the full history behind it is present.
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
