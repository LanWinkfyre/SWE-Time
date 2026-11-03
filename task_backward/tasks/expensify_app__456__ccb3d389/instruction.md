# Locate the commit that introduced this regression

A regression was reported against `Expensify/App`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Android scroll performance is really bad IF text selection is enabled

## Problem
There was a regression in Android scroll speed. On 8/25 the scroll speed was acceptable, and on the latest `master` is really slow.

## Solution
Run a `git bisect` and figure out what broke it

cc @quinthar 



I can confirm that applying this diff to `master` brings the scroll speed back to normal:

```diff
diff --git a/src/page/home/report/ReportActionItemFragment.js b/src/page/home/report/ReportActionItemFragment.js
index 246bbc5..12b9c09 100644
--- a/src/page/home/report/ReportActionItemFragment.js
+++ b/src/page/home/report/ReportActionItemFragment.js
@@ -61,7 +61,6 @@ class ReportActionItemFragment extends React.PureComponent {
                 return fragment.html !== fragment.text
                     ? (
                         <HTML
-                            textSelectable
                             renderers={this.customRenderers}
                             baseFontStyle={webViewStyles.baseFontStyle}
                             tagsStyles={webViewStyles.tagStyles}
@@ -70,11 +69,10 @@ class ReportActionItemFragment extends React.PureComponent {
                             alterNode={this.alterNode}
                         />
                     )
-                    : <Text selectable>{Str.htmlDecode(fragment.text)}</Text>;
+                    : <Text>{Str.htmlDecode(fragment.text)}</Text>;
             case 'TEXT':
                 return (
                     <Text
-                        selectable
                         style={[styles.chatItemMessageHeaderSender]}
                     >
                         {Str.htmlDecode(fragment.text)}
```
```

## What you have

- `/testbed/repo` is a git clone of `Expensify/App` truncated just after the regression was
  reported.  `HEAD` is `c61f211f308e6f453abc00584a84871d39079a09` and the full history behind it is present.
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
