# Locate the commit that introduced this regression

A regression was reported against `microsoft/TypeScript`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
mongoose has assignability error 

To repro: `cd DefinitelyTyped/types/mongoose && tsc`; observe that there are 74 errors, 2 more than the expected 72.

```ts
const locationSchema = new mongoose.Schema({
  name: { type: String, required: true },
  address: String,
  rating: { type: Number, "default": 0, min: 0, max: 5 },
  facilities: [String],
  coords: { type: [Number], index: "2dsphere" },
  openingTimes: [mongoose.Schema.Types.Mixed],
  reviews: [mongoose.SchemaTypes.Mixed],
  notes: [noteSchema]
});
var LocModel = mongoose.model<Location>("Location", locationSchema);
LocModel.create({ address: "foo", coords: [1, 2], facilities: ["foo", "bar"], name: "bar", openingTimes: ["foo"], rating: 10, reviews: ["foo"], notes: [] });
```

Actual:

At mongoose/test/model.ts:613, errors on openingTimes and reviews:

```
ERROR: 613:107  expect  TypeScript@4.2 compile error: 
No overload matches this call.
  The last overload gave the following error.
    Type 'string' is not assignable to type 'never'.
      Type 'string' is not assignable to type 'never'.
```

Expected: No error; the input type was `[mongoose.SchemeTypes.Mixed]`, which should result in `string[]` not `never[]`




Minimal repro:

```typescript
type T = any extends number ? 1 : 0;
let x: T;
x = 1;
x = 0;
```

This used to typecheck, but now `T` is `1`. The commit that changed this behavior is:
```

## What you have

- `/testbed/repo` is a git clone of `microsoft/TypeScript` truncated just after the regression was
  reported.  `HEAD` is `368cdfd29ace559e257a3c92b12212c626a5a692` and the full history behind it is present.
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
