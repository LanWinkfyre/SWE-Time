# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
RGB issue with assets and shaders borders

[Got the color inverted with handled borders.](http://postimg.org/image/l7041gazh/)
It's the same with cg or glsl.
Happening with nightly compiled just now on win7 x64 nvidia gtx 770.

Didn't happen on 12/21 nightly.

Perhaps related to @loganmc10 recent modifications?

You'll have to forgive me, what's wrong with that image? And what is the name of the shader you're having an issue with?

[It should be like this (RGB logo and blue button on the Game Gear).](http://postimg.org/image/hqhxpy57r/)

It's a shader located in shaders_xx\handheld\console-border\gg-4x.xx

I'm calling to you as I saw you tried to fix some RGB/BGR color problems.

I confirm I'm experiencing the same problem with the visualization of some assets, namely some icons in the XMB UI which currently exhibit inverted blue and red colors.

Before (build from 29/12 - proper colors for the Famicom icons): http://imgur.com/a/rgTgA
After (build from 31/12 - inverted colors): http://imgur.com/a/Ao4R4




@Ryunam can you tell us what git version your build has? I'm not able to reproduce this with the latest code, at least on Linux,
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `5d9934d4da8183a78286e8f6841d5f4b9ed72960` and the full history behind it is present.
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
