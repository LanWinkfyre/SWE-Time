# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Compile options diagnostics not displayed

Compiler options error messages are not logged to the terminal in current TSC nightly builds.

STR:
1. With typescript 1.6.0-dev.20150725, run `tsc -m commonjs -t es6 test.ts --noEmitOnError` where test.ts is an empty file

Expected Result: Error message about combining commonjs with es6 (`error TS1204: Cannot compile modules into 'commonjs', 'amd', 'system' or 'umd' when targeting 'ES6' or higher.`)

Actual result: No error, but program exits with status 1

In `compiler/program.ts`, `emitWorker()` gets a list of pre-emit diagnostics but then doesn't return them:

```
function emitWorker(program: Program, sourceFile: SourceFile, writeFileCallback: WriteFileCallback, cancellationToken: CancellationToken): EmitResult {
            // If the noEmitOnError flag is set, then check if we have any errors so far.  If so,
            // immediately bail out.  Note that we pass 'undefined' for 'sourceFile' so that we
            // get any preEmit diagnostics, not just the ones
            if (options.noEmitOnError && getPreEmitDiagnostics(program, /*sourceFile:*/ undefined, cancellationToken).length > 0) {
                return { diagnostics: [], sourceMaps: undefined, emitSkipped: true };
            }
```

Changing that to:

```
// If the noEmitOnError flag is set, then check if we have any errors so far.  If so,
            // immediately bail out.  Note that we pass 'undefined' for 'sourceFile' so that we
            // get any preEmit diagnostics, not just the ones
            let preEmitDiagnostics = getPreEmitDiagnostics(program, /*sourceFile:*/ undefined, cancellationToken);
            if (options.noEmitOnError && .length > 0) {
                return { diagnostics: preEmitDiagnostics, sourceMaps: undefined, emitSkipped: true };
            }
```

Results in the diagnostics being reported. Is this the correct fix?






It looks like there aren't any tests that exercise `ts.executeCommandLine()` directly at the moment. Where would be the best place to put those?
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `5bb2e2f584985b6b66a5ac337578fd1982f666c5` and the full history behind it is present.
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
