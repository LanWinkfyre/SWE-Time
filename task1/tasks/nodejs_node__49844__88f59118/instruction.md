# Locate the commit that introduced this regression

A regression was reported against `nodejs/node`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Unable to deserialize cloned data

### Version

main

### Platform

Linux h4ad 5.15.0-82-generic #91~20.04.1-Ubuntu SMP Fri Aug 18 16:24:39 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux

### Subsystem

js_transferable

### What steps will reproduce the bug?

To reproduce, build the NodeJS on the main branch, add the following benchmark inside `perf_hooks` folder with the name of `histogram.js`:

```js
'use strict';

const assert = require('assert');
const common = require('../common.js');

const { createHistogram } = require('perf_hooks');

const bench = common.createBenchmark(main, {
  n: [1e4],
  operation: ['creation', 'clone'],
});

let _histogram;

function main({ n, operation }) {
  switch (operation) {
    case 'creation': {
      bench.start();
      for (let i = 0; i < n; i++)
        _histogram = createHistogram();
      bench.end(n);

      // Avoid V8 deadcode (elimination)
      assert.ok(_histogram);
      break;
    }
    case 'clone': {
      bench.start();
      for (let i = 0; i < n; i++)
        _histogram = structuredClone(createHistogram());
      bench.end(n);

      // Avoid V8 deadcode (elimination)
      assert.ok(_histogram);
      break;
    }
    default:
      throw new Error(`Unsupported operation ${operation}`);
  }
}
```

Then run the benchmark with the command:

> node benchmark/compare.js --filter histogram.js --old ./out/Release/node --new ./out/Release/node perf_hooks

### How often does it reproduce? Is there a required condition?

This error doesn't throw every time you call `structuredClone`, you will be able to find it more frequently running the `benchmark`, if you run the benchmark directly, without `compare.js`, you will need to run at least 10x to be able to see the issue, is very weird.

### What is the expected behavior? Why is that the expected behavior?

The cloning always works, instead of throwing errors randomly.

### What do you see instead?

```
"new","perf_hooks/histogram.js","operation='creation' n=10000",94286.57932467105,0.106059633
node:internal/worker/io:409
  const message = receiveMessageOnPort_(port?.[kHandle] ?? port);
                  ^

Error: Unable to deserialize cloned data.
    at receiveMessageOnPort (node:internal/worker/io:409:19)
    at structuredClone (node:internal/structured_clone:24:10)
    at main (/home/h4ad/Projects/opensource/node-copy-3/benchmark/perf_hooks/histogram.js:30:22)
    at /home/h4ad/Projects/opensource/node-copy-3/benchmark/common.js:54:9
    at process.processTicksAndRejections (node:internal/process/task_queues:77:11)

Node.js v21.0.0-pre
```

### Additional information



So, @legendecas, maybe you have some hints about what is happening here.
```

## What you have

- `/testbed/repo` is a git clone of `nodejs/node` truncated just after the regression was
  reported.  `HEAD` is `c9e72e34abec1eb29fcaae3bf56fb4db76b532ec` and the full history behind it is present.
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
