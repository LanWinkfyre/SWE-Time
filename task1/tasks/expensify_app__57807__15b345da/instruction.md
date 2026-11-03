# Locate the commit that introduced this regression

A regression was reported against `Expensify/App`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Due for payment 2025-04-03] Report- Report view shakes after returning from Reports & bottom tab moves after saving search

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding and email contributors@expensify.com to request to join our Slack channel!
___

**Version Number:** 9.1.9-0
**Reproducible in staging?:** Yes
**Reproducible in production?:** No
**If this was caught on HybridApp, is this reproducible on New Expensify Standalone?:** N/A
**If this was caught during regression testing, add the test name, ID and link from TestRail:** Exp
**Email or phone of affected tester (no customers):** applausetester+ps309@applause.expensifail.com
**Issue reported by:** Applause Internal Team
**Device used:** Mac 15.3 / Chrome
**App Component:** Chat Report View

## Action Performed:
Bug 1:

1. Go to staging.new.expensify.com
2. Go to workspace chat. 
3. Submit an expense.
4. Go to Reports.
5. Go to Inbox.
6. If the display is wide, page zoom in might be required to reproduce this issue.

Bug 2:
1. Go to staging.new.expensify.com
2. Go to Reports.
3. Click Filters.
4. Apply filter that will return results.
5. Click Save search.

## Expected Result:
Bug 1: Report view will not shake after returning from Reports.
Bug 2: Bottom tab on LHN will not move after saving search.

## Actual Result:
Bug 1: Report view shakes after returning from Reports.
Bug 2: Bottom tab on LHN moves after saving search.

## Workaround:
Unknown

## Platforms:
- [ ] Android: Standalone
- [ ] Android: HybridApp
- [ ] Android: mWeb Chrome
- [ ] iOS: Standalone
- [ ] iOS: HybridApp
- [ ] iOS: mWeb Safari
- [x] MacOS: Chrome / Safari
- [x] MacOS: Desktop

## Screenshots/Videos

https://github.com/user-attachments/assets/aa85ece6-a950-448a-bd29-cfd310b5df1f

https://github.com/user-attachments/assets/2cef7cba-5ca3-4ee4-92d3-bc15ae573cee

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)

<details><summary>Issue Owner</summary>Current Issue Owner: @RachCHopkins</details>

I try to bisect from `v9.1.8-1` to `v9.1.9-0`.
```

## What you have

- `/testbed/repo` is a git clone of `Expensify/App` truncated just after the regression was
  reported.  `HEAD` is `da2fa62658cb833cfc13fc75949aa62d11fb4338` and the full history behind it is present.
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
