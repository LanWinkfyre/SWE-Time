# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[google_maps_flutter] iOS TileOverlay stops loading tiles after backgrounding app (3.13+)

### Is there an existing issue for this?

- [X] I have searched the [existing issues](https://github.com/flutter/flutter/issues)
- [X] I have read the [guide to filing a bug](https://flutter.dev/docs/resources/bug-reports)

### Steps to reproduce

1. Run the google_maps_flutter example app on an iOS device (compile against a 3.13 or higher flutter; this does not occur in 3.10) 
2. Select the Tile Overlay example
3. Click Add Tile Overlay
4. Scroll the map, and observe how the custom tiles are loaded as expected
5. Background the app (can just trigger multitasking partially, for example)
6. Scroll the map again
7. Note that no new overlay tiles are downloaded, and the only tiles shown are the ones pulled down in steps 3-4

### Expected results

As the user scrolls the map, custom TileOverlay tiles should continue to download and show whether or not the user has backgrounded the app yet.

### Actual results

As soon as the user backgrounds the app, no more custom TileOverlay tiles will download.

This issue does not occur when compiling against Flutter 3.10. It does not seem to occur on Android.

### Code sample

Reproduced using the example app in the packages repo: https://github.com/flutter/packages/tree/main/packages/google_maps_flutter/google_maps_flutter/example

### Screenshots or Video

The following was captured from an iPhone 11 running iOS 17.0. I also reproduced it on an iPad Pro running iPadOS 16.7.
<details>
<summary>Video demonstration</summary>


https://github.com/flutter/flutter/assets/602697/81a6820d-0d18-4369-933e-00bf1bb0acd8


</details>


### Logs

<details><summary>Logs</summary>



Those ((null)) console messages begin once you start scrolling the map after backgrounding/foregrounding the app, and they keep generating after that point whenever you scroll the map again.
</details>


### Flutter Doctor output

The output below is for 3.13.3, but I've reproduced it with 3.13.5 as well. The issue does not occur with 3.10.7.

<details><summary>Doctor output</summary>



</details>


Thank you @stuartmorgan for the assistance. I bisected the `master` branch of Flutter down to this commit:





Please let me know if there is anything else I can do to help.
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `45e4a0e5250c8ed21aa2d13fc2ce668aba11f186` and the full history behind it is present.
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
