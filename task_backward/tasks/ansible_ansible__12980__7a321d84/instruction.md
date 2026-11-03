# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[v2] broke my custom module tests

**Ansible Version**: 2.0.0
**Summary**:

I've a [custom module to manipulate .ini files](https://gist.github.com/mgedmin/aa629d5a4c5fe143a2ed).  I wrote some tests for it.  The first test checks that the module fails when some arguments are missing.  [This test](https://gist.github.com/mgedmin/aa629d5a4c5fe143a2ed) looks like this:

``` yaml
   - ini_file_ex: dest=/tmp/inifile
     register: out
     failed_when: not out.failed
```

Essentially, I want to invert the normal failure status.

This does not work with Ansible 2.0.0:

```
$ ansible-playbook test-ini-file-ex.yml

PLAY ***************************************************************************

TASK [command] *****************************************************************
changed: [localhost]

TASK [ini_file_ex dest=/tmp/inifile] *******************************************
/home/mg/src/deployments/provisioning/action_plugins/ini_file_ex.py:3: RuntimeWarning: Parent module 'ansible.plugins.action' not found while handling absolute import
  from ansible.plugins.action.normal import ActionModule
fatal: [localhost]: FAILED! => {"changed": false, "failed": true, "failed_when_result": true, "msg": "section or option required when state=present"}

PLAY RECAP *********************************************************************
localhost                  : ok=1    changed=1    unreachable=0    failed=1   
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `b97887ba4103acbacda7a99b3115a5a112788a51` and the full history behind it is present.
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
