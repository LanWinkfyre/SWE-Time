# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TS 3.4: Error when passing dynamically imported generic type as a function argument

<!-- 🚨 STOP 🚨 𝗦𝗧𝗢𝗣 🚨 𝑺𝑻𝑶𝑷 🚨

Half of all issues filed here are duplicates, answered in the FAQ, or not appropriate for the bug tracker. Even if you think you've found a *bug*, please read the FAQ first, especially the Common "Bugs" That Aren't Bugs section!

Please help us by doing the following steps before logging an issue:
  * Search: https://github.com/Microsoft/TypeScript/search?type=Issues
  * Read the FAQ: https://github.com/Microsoft/TypeScript/wiki/FAQ

Please fill in the *entire* template below.
-->

<!-- Please try to reproduce the issue with `typescript@next`. It may have already been fixed. -->
**TypeScript Version:**  3.4.0-dev.201xxxxx

<!-- Search terms you tried before logging this (so others can find this issue more easily) -->
**Search Terms:** TS2322, dynamic import, dynamic import never, dynamic import generic

**Code**

     .\node_modules\.bin\tsc --jsx react --lib es2017 --strict index.tsx

```ts
// ===== page.tsx ======
import * as React from 'react'

export interface PageProps {
    title: string
}

export class Page extends React.Component<PageProps> {
    render() {
        return <div>{this.props.title}</div>
    }
}

// ===== index.tsx =====
import * as React from 'react'
import{ PageProps, Page } from './page'

export function myFunction<TProps>(loader: () => Promise<React.ComponentType<TProps>>) {

}

// No error
myFunction(() => Promise.resolve(Page))

// No error
const loader: () => Promise<React.ComponentType<PageProps>> = () => import('./page').then(m => m.Page)

// Error
myFunction(() => import('./page').then(m => m.Page))

```

**Expected behavior:**

No compile error. This was the behavior in TS 3.3 and earlier.

**Actual behavior:**

There is an error after upgrading to TS 3.4:

```
index.tsx:14:18 - error TS2322: Type 'Promise<typeof Page | ComponentClass<never, any> | FunctionComponen
t<never>>' is not assignable to type 'Promise<ComponentType<PageProps>>'.
  Type 'typeof Page | ComponentClass<never, any> | FunctionComponent<never>' is not assignable to type 'C
omponentType<PageProps>'.
    Type 'ComponentClass<never, any>' is not assignable to type 'ComponentType<PageProps>'.
      Type 'ComponentClass<never, any>' is not assignable to type 'ComponentClass<PageProps, any>'.
        Type 'PageProps' is not assignable to type 'never'.

14 myFunction(() => import('./page').then(m => m.Page))
                    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  index.tsx:4:44
    4 export function myFunction<TProps>(loader: () => Promise<React.ComponentType<TProps>>) {
                                                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    The expected type comes from the return type of this signature.
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `0830292633790a6a50a494589ac0efd0f500b59c` and the full history behind it is present.
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
