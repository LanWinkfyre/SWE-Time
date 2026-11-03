# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Getting type information for a node causes other nodes to return any for their type

# Bug Report

<!--
  Please fill in each section completely. Thank you!
-->

### 🔎 Search Terms

<!--
  What search terms did you use when trying to find an existing bug report?
  List them here so people in the future can find this one more easily.
-->

Compiler API, unexpected any

### 🕗 Version & Regression Information

<!-- When did you start seeing this bug occur?

"Bugs" that have existed in TS for a long time are very likely to be FAQs; refer to
  https://github.com/Microsoft/TypeScript/wiki/FAQ#common-bugs-that-arent-bugs

If possible, please try testing the nightly version of TS to see if it's already been fixed.
For npm: `typescript@next`
This is also the 'Nightly' version in the playground: http://www.typescriptlang.org/play/?ts=Nightly

Note: The TypeScript Playground can be used to try older versions of TypeScript.

Please keep and fill in the line that best applies:
-->
- This changed between versions 4.5.x and 4.6.x

This does not repro on 4.5.5, but repros against v4.6.2

### ⏯ Playground Link

<!--
  A link to a TypeScript Playground "Share" link which shows this behavior

  The TypeScript Workbench can be used for more complex setups, try
  https://www.typescriptlang.org/dev/bug-workbench/

  As a last resort, you can link to a repo, but these will be slower for us to investigate.
-->
[Playground link with relevant code](https://www.typescriptlang.org/play?noUncheckedIndexedAccess=true&useUnknownInCatchVariables=true&noFallthroughCasesInSwitch=true&noImplicitOverride=true#code/KYDwDg9gTgLgBAMwK4DsDGMCWEVwObAwBiSMSUwAasFAM7YoAUARgIa1U304D8AXHFowomFHgCUAlEgC2zGgG0AunADeAKDhw0OIXBgQASsAA2wdsCmz5UZXAC8cZQG5N23fDYdjZi1bmKKo4ubhRkULhewD7mHAB0MqxgjIwA+gA0cKIAJqDiDgB8am5aOih6BgAKrLAO+kamscAKOaAqPDxwAAyuWlqYCHCMrSBwADxwAIz5Gn19YeS4VTUwvX0AviVZg8MouaP2h1MzW1rLsGtzAPRXWgB6PKf11bBxJhAmznA3cJVQEGAaDAAJ5wADk7xMYLg2QgwFocBQEHgoEwehw+mBgPB0gCUDBcUYACYAMwkgCc4iePzgDyeCwizxWcAA1EMotQ6AwHEdULkEKJgNk4J0unABNMvltNnMGbgem51uJXOsgA)

### 💻 Code

<!-- Please post the relevant code sample here as well-->
```ts
export function getFutureVersion(baseVersion?: string): number[] {
  const toRelease: number[] = [];
  const baseRelease: number[] = [];
  return baseRelease.map((_, index) => {
    const toPart = toRelease[index] ?? 0;
    if (index < 1) {
      return toPart;
    }
    if (index === 1) {
      toPart;
      //  ^? any
      toPart.lol; // Property 'lol' does not exist on type 'number'.(2339)
      //  ^? any
      return toPart + (baseVersion === undefined ? 0 : 1); 
    }
    return 0;
  });
}
```

### 🙁 Actual behavior

You can see that in this repro intellisense reports the type of `toPart` as `any` even though TS also knows that it must be a number.

If I attempt to get the type of `toPart`:
```js
window.sandbox.createTSProgram().then(program => {
  program.emit()
  const ast = program.getSourceFile('/input.tsx');
  console.log(
    program.getTypeChecker().getTypeAtLocation(
      ast.statements[0].body.statements[2].expression.arguments[0].body.statements[2].thenStatement.statements[0].expression,
    ),
  );
});

// -> {checker: {…}, flags: 1, id: 1, intrinsicName: 'any', objectFlags: 0}
```

Hazarding a guess intellisense and the `^?` playground token both just use `checker.getTypeAtLocation(node)` to get the type (and `checker.typeToString` to print it).

If you switch the TS version to 4.5 then you'll see that the type is correctly printed as `number` and the above snippet logs:
```js
{checker: {…}, flags: 8, id: 14, intrinsicName: 'number', objectFlags: 0}
```

### 🙂 Expected behavior

The 4.5 behaviour is correct - `getTypeAtLocation` should return a `number` type.

### Related

https://github.com/typescript-eslint/typescript-eslint/issues/4689



Like Josh Goldberg pointed out above, when we call `getTypeAtLocation` on e.g. `toPart`, we run into a type-checking circularity, because the type of `toPart` depends on the type of its initializer, which depends on the type of the parameter `index`, and the type of the parameter depends on the contextual type of `.map`, and the type of `.map` depends on the return type of the arrow function, which depends on the type of `toPart` (because of the return statement `return toPart + (baseVersion === undefined ? 0 : 1)`).
The order in which we compute types when simply compiling the program means we don't run into this circularity.
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `b996287e00088f0dcdf138b363a4b84d4b98a403` and the full history behind it is present.
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
