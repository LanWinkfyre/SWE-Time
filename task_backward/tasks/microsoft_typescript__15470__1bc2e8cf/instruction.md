# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Performance issue: TS2.3 is 6x slower on tuple type checking case

<!-- BUGS: Please use this template. -->
<!-- QUESTIONS: This is not a general support forum! Ask Qs at http://stackoverflow.com/questions/tagged/typescript -->
<!-- SUGGESTIONS: See https://github.com/Microsoft/TypeScript-wiki/blob/master/Writing-Good-Design-Proposals.md -->

**TypeScript Version:**  2.3.0 and higher

**Code**

```ts
// tupleTypeCheckingBug.ts
function scaleTime<Range, Output>(): ScaleTime<Range, Output> {
  return undefined;
}
interface InterpolatorFactory<T, U> {
  (a: T, b: T): ((t: number) => U);
}
interface TimeInterval {
  (date: Date): Date;
  floor(date: Date): Date;
  round(date: Date): Date;
  ceil(date: Date): Date;
  offset(date: Date, step?: number): Date;
  range(start: Date, stop: Date, step?: number): Date[];
  filter(test: (date: Date) => boolean): TimeInterval;
}
interface CountableTimeInterval extends TimeInterval {
  count(start: Date, end: Date): number;
  every(step: number): TimeInterval | null;
}
interface ScaleTime<Range, Output> {
  (value: Date | number | { valueOf(): number }): Output;
  invert(value: number | { valueOf(): number }): Date;
  domain(): Date[];
  domain(domain: Array<Date | number | { valueOf(): number }>): this;
  range(): Range[];
  range(range: Range[]): this;
  rangeRound(range: Array<number | { valueOf(): number }>): this;
  clamp(): boolean;
  clamp(clamp: boolean): this;
  interpolate(): InterpolatorFactory<any, any>;
  interpolate(interpolate: InterpolatorFactory<Range, Output>): this;
  interpolate<NewOutput>(interpolate: InterpolatorFactory<Range, NewOutput>): ScaleTime<Range, NewOutput>;
  ticks(): Date[];
  ticks(count: number): Date[];
  ticks(interval: TimeInterval): Date[];
  tickFormat(): ((d: Date) => string);
  tickFormat(count: number, specifier?: string): ((d: Date) => string);
  tickFormat(interval: TimeInterval, specifier?: string): ((d: Date) => string);
  nice(): this;
  nice(count: number): this;
  nice(interval: CountableTimeInterval, step?: number): this;
  copy(): this;
}

let rangeX: [number, number] = [1, 2]; // if we change type to number[] - everything works like in 2.2
let domainBounds: [number, number] = [100, 200];

let scale: ScaleTime<number, number> = scaleTime<number, number>()
  .domain([domainBounds[0], domainBounds[1]])
  .rangeRound(rangeX);
```

**Expected behavior:**
Compilation time like in typescript 2.2.2 (about 1,6s on my machine)

**Actual behavior:**
Compilation time of about 10s on typescript 2.3.0, 2.3.3, about 12s on 2.4.0-dev.20170429

Code I've used to make tests:
```js
var ts = require('typescript');
var process = require('process');
var path = require('path');

function createCompiler(options) {
  return function compiler(fileNames) {
    var program = ts.createProgram(fileNames, options);
    var result = program.emit();
    var diagnostics = ts.getPreEmitDiagnostics(program).concat(result.diagnostics);

    return {
      result: result,
      diagnostics: diagnostics
    };
  };
}

var options = {
  noEmitOnError: true,
  noImplicitAny: true,
  target: 'es5',
  module: 'commonjs'
};
var compiler = createCompiler(options);
var fileNames = [path.join(__dirname, 'tupleTypeCheckingBug.ts')];

var started = process.hrtime();
var result = compiler(fileNames);
var elapsed = process.hrtime(started);

function ms(elapsed) {
  return Math.round(Math.round(elapsed[0] * 1E9 + elapsed[1]) / 1E6);
}

console.log('TypeScript ' + ts.version + ' time: ' + ms(elapsed) + 'ms');
```
If I change `rangeX` type to `number[]`, everything works like in 2.2.
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `7080c4155b2c6cc69c5dae3f312d720d434da3a3` and the full history behind it is present.
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
