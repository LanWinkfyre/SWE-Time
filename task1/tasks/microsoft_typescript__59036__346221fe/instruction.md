# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Include paths evaluate to no files when tsconfig.json is in a sandbox (regression in 5.5)

### 🔎 Search Terms

symlink tsconfig includes

### 🕗 Version & Regression Information

- This changed between versions 5.4.5 and 5.5.2


### ⏯ Playground Link

_No response_

### 💻 Code

_No response_

### 🙁 Actual behavior

Under Bazel, builds are made more hermetic by creating a dedicated folder (an "execroot") and symlinking files into it.

Starting in TS 5.5, we see the following minimal reproduction:

```
% npm init -y
% npm install typescript@5.5.2
% echo "export const a = 1;" > index.ts
% echo "{}" > tsconfig.json
% mkdir execroot
% cd execroot
execroot % ln -s ../index.ts . 
execroot % ln -s ../tsconfig.json .
execroot % ../node_modules/.bin/tsc -p tsconfig.json --outDir .
error TS18003: No inputs were found in config file '/Users/alexeagle/repros/ts55/execroot/tsconfig.json'. 
Specified 'include' paths were '["**/*"]' and 'exclude' paths were '["/Users/alexeagle/repros/ts55/execroot"]'.


Found 1 error.
```

Note that if `--outDir .` is removed, then this command instead succeeds and writes `index.js`.



### 🙂 Expected behavior

In the prior TypeScript release this was working.

### Additional information about the issue



Using https://www.npmjs.com/package/every-ts:
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `ef339af12801c1f88ff4e01d4d4e602addfcca98` and the full history behind it is present.
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
