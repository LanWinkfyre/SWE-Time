# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TypeScript 4.6 sometimes treats tuple union types as "never" when switch-case has a "default" clause

# Bug Report

The error described below started with TypeScript 4.6.1-rc. A minimal repro is included.

### 🔎 Search Terms

- Destructuring
- Union types

### 🕗 Version & Regression Information

- This changed between versions 4.5.5 and 4.6.1-rc

### ⏯ Playground Link

[Playground link with relevant code](https://www.typescriptlang.org/play?ts=4.6.0-dev.20220116#code/KYDwDg9gTgLgBDAnmYcCi4rAM7YJYQB2cAvHAEIQQA2wAhoQDIQDmeAxhmFrgcQD5wA5DCgBXYELiChAMzrVskgNwAoUJFgJkqSjXpNWHLj3xFScANpCGAEyEAaOADpXJnGcKWAut+lWhQggYR3RMDz5vNXVwaHhZMUJ2GD44YAA3BTE6GGAACg1TPgAuMO4IogBKUoAjKloGOABvVTg4PFk4PIBBKCg6RGc8bF7+xALw3irK5ta2uHYibHhLCBR+mGgnV2c14H7CW2w-MkKKwjV5uGwAdzwYdgALLr2N6BmWq7b2OiVhOyEpU+XzaWBgYigxFedmwzgy+3GeSeeGothmJAAfGlMtRsrkkY8UWjKpcvgBfOZXH5-QLBQGzEGg4DgyFwACEGSyOXy0MO2EsAAZvCTKfMKSDbMB5GJqDAgaKrjBHlAIDc4IRgGq0H1oHkAAYAEia0M2UDJ7Ww6uCcDo1zEYE0uVscBN0D1IpB4rFc3NwEUqGBTJZxDOU2IJAjwlEEiEpIpZKAA)

### 💻 Code

See this toy NAND evaluator. Something about the recursive union type causes TS to fail when destructuring the array. Deleting the `default` clause causes the error to go away. (The `default` clause is unnecessary if assuming TS is sound but one can see why a safety net is helpful.)

```ts
export type Expression = BooleanLogicExpression | 'true' | 'false';
export type BooleanLogicExpression = ['and', ...Expression[]] | ['not', Expression];

export function evaluate(expression: Expression): boolean {
  if (Array.isArray(expression)) {
    const [operator, ...operands] = expression;
    switch (operator) {
      case 'and': {
        return operands.every((child) => evaluate(child));
      }
      case 'not': {
        return !evaluate(operands[0]);
      }
      default: {
        throw new Error(`${operator} is not a supported operator`);
      }
    }
  } else {
    return expression === 'true';
  }
}
```

### 🙁 Actual behavior

The line `const [operator, ...operands] = expression;` produces the error: `TS2488: Type 'never' must have a '[Symbol.iterator]()' method that returns an iterator.`

### 🙂 Expected behavior

Expected there not to be an TS error.
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `67d376c882bcf4318a459c9a504287fc449e7847` and the full history behind it is present.
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
