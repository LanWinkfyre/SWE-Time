# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
New parameter implicit any error with latest nightly

# Bug Report

from https://github.com/microsoft/TypeScript/issues/52148#issuecomment-1376138875

### 🔎 Search Terms

- Implicit any
- parameter

### 🕗 Version & Regression Information


- This changed between versions 4.9.4 and 5.0.0-dev.20230111

### ⏯ Playground Link

https://www.typescriptlang.org/play?ts=5.0.0-dev.20230111#code/CYUwxgNghgTiAEAzArgOzAFwJYHtXzDigxAElUBnDKdEAHgGEMcZ4QAPE1YC+VEAO7wAFADpxsAOYUAXPBoBPANoBdAJTwAvAD55qBQBp4AJTacQ3XuSo0wIACoKADvSYtt24ZhZy3MI+KiUrLwDHhUMMjeMAAKsFAAtiAkMBSMzDDaanLGANwAUPkcTiwY8FioKYhQdvCkALIWyADqLADWAEYWYAAW9jg4EABCsADyTtjh8ADe+fDz8MyDHWMTuJRyswvbSAPCKzByERWS2fDHqJJzCwC+BTeFkFAUvI2oLe1d6H0Dw7Az13mYHCGEi0WEgJ2ODW4TkDSarRgnW6P0GIxg40mlHgAB94GhQIgKiBgAZIRppvAHg98oQQMQyJRqLRhG8Pkivr1+mjYEYtgslhADpj1iF+Ttdjh9rAKfA4BhkDB8AdclTIdS1LkgA

### 💻 Code

<!-- Please post the relevant code sample here as well-->
```ts
declare function createInstance<Ctor extends new (...args: any[]) => any, R extends InstanceType<Ctor>>(ctor: Ctor, ...args: ConstructorParameters<Ctor>): R;

export interface IMenuWorkbenchToolBarOptions {
    toolbarOptions: {
        foo(bar: string): string
    };
}

class MenuWorkbenchToolBar {
    constructor(
        options: IMenuWorkbenchToolBarOptions | undefined,
    ) { }
}

createInstance(MenuWorkbenchToolBar, {
    toolbarOptions: {
        foo(bar) { return bar; } // error here
    }
});
```

### 🙁 Actual behavior

`bar` implicitly has an `any` type

### 🙂 Expected behavior

`bar` should be inferred to be a string

/cc @RyanCavanaugh 

This seems unintentional:





@ahejlsberg
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `a05b7ec01fc9f1a8001e4556b56a151246b75f2c` and the full history behind it is present.
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
