# Locate the commit that introduced this regression

A regression was reported against `Expensify/App`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Due for payment 2026-07-13] [$250] Withdrawal amount overlaps with subtitle content on mobile Bank Reconciliation screen

If you haven’t already, check out our [contributing guidelines](https://github.com/Expensify/ReactNativeChat/blob/main/contributingGuides/CONTRIBUTING.md) for onboarding. To join our Slack channel, fill out [this form](https://forms.gle/Q7hnhUJPnQCK7Fe56).
___

**Version Number:** 94.17-0
**Reproducible in staging?:** Y
**Reproducible in production?:** Y
**If this was caught during regression testing, add the test name, ID and link from BrowserStack:**
**Email or phone of affected tester (no customers):**
**Logs:** https://stackoverflow.com/c/expensify/questions/4856
**Expensify/Expensify Issue URL:**
**Issue reported by:** @dubielzyk-expensify 
**Slack conversation** (hyperlinked to channel name): [#Expensify Bugs](https://expensify.slack.com/archives/C049HHMV9SM/p1782184748171849)

## Action Performed:

1. Open New Expensify on a mobile device.
2. Navigate to Spend > Bank Reconciliation.
3. View the list of withdrawal entries.
4. Observe entries with long subtitle content (e.g., withdrawal date and withdrawal ID).

## Expected Result:
The withdrawal amount should remain clearly visible without overlapping or crowding the subtitle content.
The subtitle should truncate appropriately before reaching the amount column.
## Actual Result:
The withdrawal amount visually clashes with the subtitle text, causing layout crowding and reducing readability.
## Workaround:
Unknown
## Platforms:
Select the officially supported platforms where the issue was reproduced:
- [ ] Android: App
- [ ] Android: mWeb Chrome
- [x] iOS: App
- [ ] iOS: mWeb Safari
- [ ] iOS: mWeb Chrome
- [ ] Windows: Chrome
- [ ] MacOS: Chrome / Safari

## Screenshots/Videos

<img width="400" height="1000" alt="Image" src="https://github.com/user-attachments/assets/50a82e24-62b9-494a-ab50-6e94dd908ff2" />

<img width="300" height="700" alt="Image" src="https://github.com/user-attachments/assets/bc184cef-d8be-47b3-9d81-395404cf905b" />

[View all open jobs on GitHub](https://github.com/Expensify/App/issues?q=is%3Aopen+is%3Aissue+label%3A%22Help+Wanted%22)

<details><summary>Upwork Automation - Do Not Edit</summary>
    <ul>
        <li>Upwork Job URL: <a href="https://www.upwork.com/jobs/~022070682951797679594">https://www.upwork.com/jobs/~022070682951797679594</a></li>
        <li>Upwork Job ID: 2070682951797679594</li>
        <li>Last Price Increase: 2026-06-27</li>
    </ul>
</details>

<details><summary>Issue Owner</summary>Current Issue Owner: @mallenexpensify</details>





<details>
<summary>Evidence</summary>





</details>
```

## What you have

- `/testbed/repo` is a git clone of `Expensify/App` truncated just after the regression was
  reported.  `HEAD` is `1d88d349ddaa8ff17d0c1e5e16e9adb9c0a2e3a1` and the full history behind it is present.
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
