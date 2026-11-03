# Locate the commit that introduced this regression

A regression was reported against `mastodon/mastodon`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
TypeError (can't access property "size") when rendering the report modal

### Steps to reproduce the problem

1. Try to report a post

### Expected behaviour

Reports work

### Actual behaviour

Reports do not work

### Specifications

Happening on mastodon.social (since the latest update that merges the logged-out web app PRs, presumably.)

```
TypeError: can't access property "size", a is undefined


render@https://static-cdn.mastodon.social/packs/js/modals/report_modal-b792d6d60f2c515806e5.chunk.js:1:1678
Bi@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1052427
qi@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1052222
ks@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1087836
bl@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1079279
ml@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1079202
sl@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1076232
Yo/<@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1027873
t.unstable_runWithPriority@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1102929
Vo@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1027582
Yo@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1027820
Xo@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1027753
nl@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1073017
enqueueSetState@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:1031538
_.prototype.setState@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:977464
l/this.load/<@https://static-cdn.mastodon.social/packs/js/common-1f5f9a3dfb3f14cff9ca.js:2:238678



render (webpack:///app/javascript/mastodon/features/report/category.js:66:20)
expirationTime (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:3677:14)
expirationTime (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:3665:16)
ng (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:5863:19)
Mi (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:5231:)
Ri (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:5228:131)
Ii (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:5002:)
Ie (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:2056:44)
Wg (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:6810:6)
Ee (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:2032:)
He (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:2050:15)
He (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:2044:44)
hh (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:4867:222)
bf (webpack:///node_modules/react-dom/cjs/react-dom.production.min.js:2267:29)
props (webpack:///app/javascript/mastodon/components/media_gallery.js:247:16)
this.setState (webpack:///app/javascript/mastodon/features/ui/components/bundle.js:73:43)
```
```

## What you have

- `/testbed/repo` is a git clone of `mastodon/mastodon` truncated just after the regression was
  reported.  `HEAD` is `402ee73e24ea816ab1602405cd0046ecd5e7bfd5` and the full history behind it is present.
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
