# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Branch picker loses focus with vim mode

### Reproduction steps

1. Ensure vim mode is enabled
2. Open an empty project with a git repo initialized (can use [this repo](https://github.com/mchisolm0/repro-repo#))
3. Open the git panel
4. Click on the branch selector between the repo name and the "Fetch" button
5. Press `i` to try typing the letter `i`
6. Observe no letter is typed, the branch selector closes, and the commit message box gets focus

#### Other notes
I notice other keypresses also do not have expected behavior, for example:
- `j` and `k` move up and down the branch list rather than typing `j` or `k`. I would expect `ctrl-j` and `ctrl-k` to have that behavior.
- `x` shows no visible feedback
- At the 17 seconds mark in the below video, I show the same keypresses working in the branch selector in Zed's header section even though it does not work in the git panel

Not sure these are related, but I wanted to call them out.

<details><summary>Video of bug</summary>

https://github.com/user-attachments/assets/bc389c7a-8f01-42ee-a873-c2feab0f4f7d

</details>

### Current vs. Expected behavior

Current behavior: The branch selector loses focus and the commit editor gains focus when trying to type `i` in the branch selector.

Expected behavior: Can type `i` in the branch selector to either search for a branch with `i` in the name or create a branch with `i` in the name.

### Zed version and system specs


OS: macOS 26.2
Memory: 16 GiB
Architecture: aarch64

### Attach Zed log file

<details><summary>Zed.log</summary>

<!-- Paste your log inside the code block. -->


</details>


### Relevant Zed settings

<details><summary>settings.json</summary>
Reproduced with only vim mode set

<!-- Paste your settings inside the code block. -->
```json
{ "vim_mode": true }
```

</details>


### Relevant Keymap

<details><summary>keymap.json</summary>
Reproduced with a blank keymap file.

<!-- Paste your keymap file inside the code block. -->
```json
[]
```

</details>


### (for AI issues) Model provider details

N/A

### If you are using WSL on Windows, what flavor of Linux are you using?

None

 

not reproducible on stable 0.229.0 because it doesn't include that commit
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `54a95e717d4ed1589c9b0e38648f65424defc74b` and the full history behind it is present.
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
