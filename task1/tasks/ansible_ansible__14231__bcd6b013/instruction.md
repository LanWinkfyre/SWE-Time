# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
'ansible_os_family' is undefined

All playbooks with ansible_os_family used for conditional roll includes now fail. 

I don't see anything regarding the renaming of the ansible_os_family variable so I assume this is a bug?





```
fatal: [testing]: FAILED! => {"failed": true, "msg": "The conditional check 'ansible_os_family == 'Debian'' failed. The error was: error while evaluating conditional (ansible_os_family == 'Debian'): 'ansible_os_family' is undefined\n\nThe error appears to have been in '/Users/tanner/projects/ansible.git/playbooks.git/roles/updates/tasks/main.yml': line 4, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n- include: debian.yml\n  ^ here\n"}
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `49c15c81376c258d130cd0f89c6ff25467ebf17b` and the full history behind it is present.
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
