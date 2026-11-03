# Locate the commit that introduced this regression

A regression was reported against `ray-project/ray`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[rllib] Vectorization & multi-agent are broken in DDPG (both TF and Torch)

<!--Please include [tune], [rllib], [autoscaler] etc. in the issue title if relevant-->

### What is the problem?

`./train.py --run=DDPG --env=MountainCarContinuous-v0 --config='{"num_envs_per_worker": 2}'`
and
`./train.py --run=DDPG --env=MountainCarContinuous-v0 --config='{"num_envs_per_worker": 2}' --torch`

both currently crash. The issue seems to be that while the input to compute_actions() is a batch of N observations, only 1 action is returned as output. I ran into this while debugging a hang in a multi-agent test case (hung due to a bug in the env triggered by vectorization returning 1 action instead of N actions).





script:
```
cd python
sudo SKIP_THIRDPARTY_INSTALL=1 SKIP_PYARROW_INSTALL=1 python setup.py develop
cd -
cd rllib
./train.py --run=DDPG --env=MountainCarContinuous-v0 --config='{"num_envs_per_worker": 2}' --stop='{"timesteps_total": 1}'
```
```

## What you have

- `/testbed/repo` is a git clone of `ray-project/ray` truncated just after the regression was
  reported.  `HEAD` is `cc7bd6650ae88aa7fd1ce43b0ca71c869c08557a` and the full history behind it is present.
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
