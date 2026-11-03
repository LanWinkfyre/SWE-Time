# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
The error was: 'ansible_env' is undefined

<!--- Verify first that your issue is not already reported on GitHub -->
<!--- Also test if the latest release and devel branch are affected too -->
<!--- Complete *all* sections as described, this form is processed automatically -->

##### SUMMARY
he error was: 'ansible_env' is undefined

##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME
debug

##### ANSIBLE VERSION


##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
```paste below
$ ansible-config dump --only-changed
<nothing>
```

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->
Management host macOS 10.12.6
Managed host Windows 10 64-bit

##### STEPS TO REPRODUCE

<!--- Paste example playbooks or commands between quotes below -->
```yaml
- debug:
    msg: "{{ ansible_env }}"
```
##### EXPECTED RESULTS
Dump of the ansible_env 


##### ACTUAL RESULTS
<!--- Describe what actually happened. If possible run with extra verbosity (-vvvv) -->

<!--- Paste verbatim command output between quotes -->
```paste below
FAILED! => {"msg": "The task includes an option with an undefined variable. The error was: 'ansible_env' is undefined\n\nThe error appears to have been in '/Users/tanner/projects/ansible.git/playbooks.git/roles/win_common/tasks/main.yml': line 65, column 3, but may\nbe elsewhere in the file depending on the exact syntax problem.\n\nThe offending line appears to be:\n\n\n- debug:\n  ^ here\n"}
```


Git bisect tells me this:



And yes, I'm running ansible with --tags and I don't see [Gather Facts] running when I do --tags.
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `17b3171917d85dd622bc96366bbdfecf8498718d` and the full history behind it is present.
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
