# Locate the commit that introduced this regression

A regression was reported against `Expensify/App`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
VBA - Continuous loading spinner appears after company information page

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/CONTRIBUTING.md) for onboarding and email contributors@expensify.com to request to join our Slack channel!
___

## Action Performed:
1. Launch the app and login
2. Go to any Workspace and tap on connect Bank account
4. Use Plaid or connect manually
5. Continue the flow up to company info page and click next

## Expected Result:
User is taken to the next page

## Actual Result:
Loading spinner appears for ever

## Workaround:
Unknown

## Platform:
<!--- 
Remove any platforms that aren't affected by this issue
--->
Where is this issue occurring?

- Web
- iOS
- Android
- Desktop App
- Mobile Web

**Version Number:** 1.1.18.0

**Reproducible in staging?:** Yes 

**Reproducible in production?:** Unable to check in production with staging credentials

**Logs:** https://stackoverflow.com/c/expensify/questions/4856

**Notes/Photos/Videos:** 



https://user-images.githubusercontent.com/43996225/145040937-e1ae7ccb-9ca0-4eaa-b887-413b691f3059.mp4

**Expensify/Expensify Issue URL:**

**Issue reported by:** Applause

**Slack conversation:** 

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)
```

## What you have

- `/testbed/repo` is a git clone of `Expensify/App` truncated just after the regression was
  reported.  `HEAD` is `673869099b13acfd28ebf798c3c44e075314bb31` and the full history behind it is present.
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
