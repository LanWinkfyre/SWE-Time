# Locate the commit that introduced this regression

A regression was reported against `Expensify/App`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[HOLD for payment 2024-07-10] [$250] Chat - Report in the background loads infinitely after refreshing group confirmation page

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding and email contributors@expensify.com to request to join our Slack channel!
___

**Version Number:** 9.0.2-0
**Reproducible in staging?:** Y
**Reproducible in production?:** N
**Logs:** https://stackoverflow.com/c/expensify/questions/4856
**Issue reported by:** Applause-Internal team


## Action Performed:
1. Go to staging.new.expensify.com
2. Go to FAB > Start chat.
3. Click Add to group next to a few users.
4. Click Next.
5. Refresh the confirmation page.
6. Dismiss the confirmation page.

## Expected Result:
In Step 5, after refreshing the confirmation page, the report in the background will load.

## Actual Result:
In Step 5, after refreshing the confirmation page, the report in the background shows infinite loading.
In Step 6, after dismissing the confirmation page, the link is https://staging.new.expensify.com/r

## Workaround:
Unknown

## Platforms:
<!---
Check off any platforms that are affected by this issue
--->
Which of our officially supported platforms is this issue occurring on?
- [ ] Android: Native
- [ ] Android: mWeb Chrome
- [ ] iOS: Native
- [ ] iOS: mWeb Safari
- [x] MacOS: Chrome / Safari
- [x] MacOS: Desktop

## Screenshots/Videos


https://github.com/Expensify/App/assets/115492554/348585e4-2042-45b2-bdec-5ba4994ff8be



</details>

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)


<details><summary>Issue Owner</summary>Current Issue Owner: @CortneyOfstad</details>

Actually, that's wrong. I tested reverting that PR on `main` and the bug is still there.





@Kicu @mountiny @roryabraham @rayane-djouah
```

## What you have

- `/testbed/repo` is a git clone of `Expensify/App` truncated just after the regression was
  reported.  `HEAD` is `0c20881a308244867119efa6196481b65bb81274` and the full history behind it is present.
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
