# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
CN characters are not displayed properly in RetroArch

## Description

CN characters are not displayed properly in RetroArch， I have tried replace to yahei and other cn supported fonts， but it doesn't work， in 1.9.0 the issue is not existed

### Expected behavior

The font display properly，not show square

### Steps to reproduce the bug

1.Default is English in retroarch, set it to cn, now you can see it display properly, 
![image](https://user-images.githubusercontent.com/10301545/113288172-2d691f80-9321-11eb-85f1-8731556eab2c.png)
but after you save the config and reboot, you can see the below:
![image](https://user-images.githubusercontent.com/10301545/113288217-3d80ff00-9321-11eb-96d2-f26b7ee2f4ba.png)

2. Then , set it back to en, you can get the below:
![image](https://user-images.githubusercontent.com/10301545/113288315-5f7a8180-9321-11eb-8a66-6fd00126fe25.png)


### Bisect Results



### Version/Commit




### Environment information

- OS: aarch64 linux




@liushuyu Do you have any idea what could cause the issue ? Chinese, Korean, Arabic and Persian languages are affected. When you restart RetroArch you got square instead of the correct display of the font.
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `21b2ec6bd528a6acc9fc145af9b057ad27213135` and the full history behind it is present.
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
