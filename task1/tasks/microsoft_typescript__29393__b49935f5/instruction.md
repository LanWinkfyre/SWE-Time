# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression: Unrelated line causes complex type check error to disappear

**TypeScript Version:**  No issue in 3.0.3, broken in both 3.2.2 and 3.3.0-dev.20190112 (using tsconfig from `tsc --init`)

<!-- Search terms you tried before logging this (so others can find this issue more easily) -->
**Search Terms:** unrelated, nondeterministic, mapped type, generic

**Code**

I'm sorry, I couldn't manage to reduce this further since it disappears when the code is too simple (probably some checking depth limitation?)

```ts
// when I replace this import by just inlining the corresponding types,
// the error disappears
import { TypeOf, Type } from "io-ts";

type ToB<S extends any> = { [k in keyof S]: TypeOf<S[k]> };
type ToA<S> = { [k in keyof S]: Type<S[k]> };

type NeededInfo<MyNamespaceSchema = {}> = {
  ASchema: ToA<MyNamespaceSchema>;
};

export const ASchema = {
  initialize: null as any
};

export type MyInfo = NeededInfo<ToB<typeof ASchema>>;

const tmp1: MyInfo = null!;
function tmp2<N extends NeededInfo>(n: N) {}
// tmp2(tmp1); // uncommenting this line removes a type error from a completely unrelated line ??

class Server<X extends NeededInfo> {}
export class MyServer extends Server<MyInfo> {} // not assignable error at `MyInfo`
```

**Expected behavior:** No type error regardless of whether the line `//tmp2(tmp1)` is commented or not.

**Actual behavior:**

When that line is commented out, I get a type error in the `export class` line, which is completely unrelated:

```
[ts]
Type 'NeededInfo<ToB<{ initialize: any; }>>' does not satisfy the constraint 'NeededInfo<{}>'.
  Types of property 'ASchema' are incompatible.
    Type 'ToA<ToB<{ initialize: any; }>>' is not assignable to type 'ToA<{}>'.
      Type '{}' is not assignable to type 'ToB<{ initialize: any; }>'. [2344]
```

**Playground Link:** Impossible because it stops happening when Type and TypeOf are inlined.

I know the above code looks dumb, but trust me this is causing weird breakage in a large code base.

I just did a git bisect because this issue is preventing me from upgrading from 3.0 to a newer version of TS. 

 

I might be able to add a test case if that would help you fix it?

bisect log:
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `fadd95f72b5ad7f7f1cffa2b6ac82f612694462c` and the full history behind it is present.
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
