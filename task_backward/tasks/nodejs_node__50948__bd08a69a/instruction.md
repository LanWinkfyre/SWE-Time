# Locate the commit that introduced this regression

A regression was reported against `nodejs/node`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
### Version

21.2.0



### Platform

Darwin moxy.lan 23.1.0 Darwin Kernel Version 23.1.0: Mon Oct  9 21:27:24 PDT 2023; root:xnu-10002.41.9~6/RELEASE_ARM64_T6000 arm64

### Subsystem

esm hooks

### What steps will reproduce the bug?

```
echo 'console.log("hello")' > x.js
echo '{}' > package.json
npm i tap
node --import=./node_modules/@tapjs/mock/dist/esm/import.mjs --import=./node_modules/@tapjs/processinfo/dist/esm/import.mjs x.js
```

### How often does it reproduce? Is there a required condition?

Always reproduces

### What is the expected behavior? Why is that the expected behavior?

Expect that it loads the two import arguments, and then runs the file.

### What do you see instead?

Deadlocks at the `Module.register()` call in the second import script.

### Additional information

Discussion from slack:

isaacs
  [7 hours ago](https://openjs-foundation.slack.com/archives/C053UCCP940/p1701105647485299)
[@aduh95](https://openjs-foundation.slack.com/team/U01CVNDJDME)
 It seems like it's getting stuck at:
```
      // Sleep until worker responds.
      AtomicsWait(this.#lock, WORKER_TO_MAIN_THREAD_NOTIFICATION, this.#workerNotificationLastId);
```
I haven't been able to narrow it down to a satisfyingly minimal reproduction, and for extra :grimacing: it's order-dependent, but this will reproduce it in any project that has the latest tap installed:
```
node --import=./node_modules/@tapjs/mock/dist/esm/import.mjs --import=./node_modules/@tapjs/processinfo/dist/esm/import.mjs x.js
```

(where x.js is just console.log('hello'))




5 replies
Jacob Smith
  [4 hours ago](https://openjs-foundation.slack.com/archives/C053UCCP940/p1701118050060099?thread_ts=1701105647.485299&cid=C053UCCP940)
Oof. These are very difficult to troubleshoot.
I think i'll have time on Wednesday to take a look (edited) 
aduh95
  [3 hours ago](https://openjs-foundation.slack.com/archives/C053UCCP940/p1701121588702959?thread_ts=1701105647.485299&cid=C053UCCP940)

:pray:
1

isaacs
  [9 minutes ago](https://openjs-foundation.slack.com/archives/C053UCCP940/p1701131493205209?thread_ts=1701105647.485299&cid=C053UCCP940)
It seems like what's going on is that the @tapjs/mock needs to make a request on its MessageChannel port in order to finish its resolve hook.
Then it loads @tapjs/processinfo/import, which calls Module.register. This triggers a sync request to the worker thread for 'register', which then triggers the mock's resolve hook to resolve the loader.mjs file, but because it's already awaiting a sync message (the register), it'll never come, because that sync message is waiting for another sync message (the resolve).
isaacs
  [4 minutes ago](https://openjs-foundation.slack.com/archives/C053UCCP940/p1701131790120899?thread_ts=1701105647.485299&cid=C053UCCP940)

isaacs
  [1 minute ago](https://openjs-foundation.slack.com/archives/C053UCCP940/p1701131928525939?thread_ts=1701105647.485299&cid=C053UCCP940)
Also: seems like it's related to the use of the MessageChannel specifically. Just a timeout doesn't trigger it, but the busywait message processing seems to keep the other message channel from proceeding.
```

## What you have

- `/testbed/repo` is a git clone of `nodejs/node` truncated just after the regression was
  reported.  `HEAD` is `95b198911382b0aa0a0448e2a86214558665e02b` and the full history behind it is present.
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
