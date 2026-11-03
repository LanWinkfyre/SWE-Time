# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Type guard and assertion do not properly refine union types with optional properties

### 🔎 Search Terms

"type guard union types narrowing"
"asserts is not refining type"
"type refinement union types bug"
"dryRun outputPath assertion"
"optional property refinement bug"

### 🕗 Version & Regression Information

This changed between versions 4.7.4 and 4.8.4.


### ⏯ Playground Link

https://www.typescriptlang.org/play/?ts=5.7.3#code/KYDwDg9gTgLgBASwHY2FAZgQwMbDgMQQBtgBnAYRMyQFcxKF8jMBzUuAbwCg5e4pgmACYQkRAJ5whUcQCUaSAPwAuOACMIEKkgDcPPgOGiJcCDRhhzABUwwAFirikYUZCz0BfLlwD0PuAAq4mB4LDSYUEJwAO4I9nAABgikCXDo0PzA6MhucAoIonAwwWRc6ArYMAVIcNh2wNgA1gxMrKQAFPq86MxsqoQkFNp0Lb2kADRcAJSqPW2I7ByZRmKS0nIKqi40wDrLIqum5pYwNvaqzq5ILHAecAA+nPvGazLySrOYRKR4d9x8iHQcHaczYADp1u84AAyaFwACEoNIYLMFmstjsU04XQBRTsUAg0TgSGARIAolACVB2gByAL1OAAWkZqJOZzspjAVUKyUyAEcaAgBFFkFIZIyoAo4ABbCBCPDUKLSmjOJwhbAIdCSex4cpEIhpYh4MAYsE0qZ6AFeAECGA0KA1ba7LheXz+ACymFF5SQlWqeVIuR1RRKcDCESEZQq3Jq0q9SHaWP+fGwolVEC51VI-SNQ0EtHoREYYzgAF5OB49DjNcC6g1mkXWmx2hmY6QpkmcQDU0hVUtIQpxkc0acMbcy5y25bcbw-HAyeAGqghKogiEAMrYVxcpx2MxEKICbIkxKtrOpGAQJ4DpBbSW7YdsjEXFy5O6PftvBSOLDfX5dvg5wAQUqcIiFXEpN23eAj2QMhT0zNNUheIor0-DZbyKe89lZdFzicV9rluSYZ1nfwIGlOIqiIhJ0PeH8vh+W5UmwTAfjBHEvFdOcAFVAxotiflgdhklSAA3NBA0KCAgWDOsmijX0Y1qeomlGNoAHU4jsIDSCEmAOhxJEc0GSh8xGRsxkmGY4EEtADLSEteSWQwDhMG87x2PZXJQ3DR3wy43weJ4fMOG8GL-cdk14GsQTGCEvxqWEESRFFjjwzFsVIvECSJElyUpaBaXpPBmT89lJ39XkBAFIVgBFGp1glKVZXlWykCVFV4FIdVNW1Bk9QNbISDgE17DNC1OJdbw509b1o39FVcjs4TFL9Qo42QLT7F0-SOk7bs03gM80xMsgzOoCzi3mcsOErbxu1UhtrrYbadL0+yOhO3tJpxHs+zFDCh3Ksc7nLb7SGnMj50XSp6ogjctwQHdSD3GgD0yY88ASCGLzQwH3k8h8QYCwibnfa9EoipjrUA-wQLtL4EeAKDkZgrI4PYHHEN7ZDDkvSmMKJnD0v8uwXyucmSLp0xKJgaiblognv0+SKPBYtjgA4rwgA

### 💻 Code

```ts
export interface FilesCleanupCliFlags {
    readonly dryRun?: boolean;
    readonly outputPath?: string;
}

// Type guard with `is` for refining union types
function checkCliFlags(
    flags: FilesCleanupCliFlags,
): flags is { readonly dryRun: true; readonly outputPath: string } | { readonly dryRun?: false } {
    if (flags.dryRun && !flags.outputPath) {
        throw new Error('The --outputPath option is required in dry-run mode and must specify the full file path.');
    }
    return true;
}

// Main function using the type guard
function main() {
    const options: FilesCleanupCliFlags = {};

    if (checkCliFlags(options)) {
        const { dryRun, outputPath } = options;
        // Expected: TypeScript should refine `options` to { dryRun: true; outputPath: string } | { dryRun?: false }
        // Actual: TypeScript refines `options` only to { dryRun: true; outputPath: string },
        // omitting `{ dryRun?: false }` case.
    }
}

// Using `asserts is` version of the check
function checkCliFlagsWithAsserts(
    flags: FilesCleanupCliFlags,
): asserts flags is { readonly dryRun: true; readonly outputPath: string } | { readonly dryRun?: false } {
    if (flags.dryRun && !flags.outputPath) {
        throw new Error('The --outputPath option is required in dry-run mode and must specify the full file path.');
    }
}

// Main function using asserts
function mainWithAsserts() {
    const options: FilesCleanupCliFlags = {};

    checkCliFlagsWithAsserts(options);

    const { dryRun, outputPath } = options;
    // Expected: TypeScript should refine `options` to { dryRun: true; outputPath: string } | { dryRun?: false }
    // Actual: TypeScript refines `options` only to { dryRun: true; outputPath: string },
    // omitting `{ dryRun?: false }` case.
}

```


### 🙁 Actual behavior

**TypeScript does not refine the type** of `options` correctly after the type guard (`checkCliFlags`) or assertion (`checkCliFlagsWithAsserts`)
  - When using `checkCliFlags(optins)` or `checkCliFlagsWithAsserts(options)`, the expected refinement is:
    ```typescript
    { readonly dryRun: true; readonly outputPath: string } | { readonly dryRun?: false }
    ```
  - However, TypeScript only refines `options` to `{ readonly dryRun: true; readonly outputPath: string }`, and the `{ dryRun?: false }` branch is omitted.

### 🙂 Expected behavior

TypeScript should refine the type of `options` to:

```typescript
{ readonly dryRun: true; readonly outputPath: string } | { readonly dryRun?: false }
```

### Additional information about the issue

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `700ee076e515db2ef49d8cf7e4dc4bf70679575c` and the full history behind it is present.
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
