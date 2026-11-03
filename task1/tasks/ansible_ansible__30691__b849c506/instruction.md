# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
any_errors_fatal still broken in ansible/stable-2.4

##### ISSUE TYPE
 - Bug Report


##### COMPONENT NAME
any_errors_fatal feature

##### ANSIBLE VERSION


##### CONFIGURATION

Default configuration

##### OS / ENVIRONMENT

macOS Sierra 10.12.6 (16G29)

##### SUMMARY
any_errors_fatal doesn't stop task execution. Basic usage

##### STEPS TO REPRODUCE
Create the following playbook:
```yaml
- hosts: all
  gather_facts: no
  any_errors_fatal: true

  tasks:
    - name: Fail a single host
      fail:
      when: inventory_hostname=="host0"
 
    - name: Run on both host
      debug: msg='Run on both host'
```

The accompanying hosts file is:
```
host0 ansible_host=127.0.0.1
host1 ansible_host=127.0.1.1
```
##### EXPECTED RESULTS

The playbook should stop at the first task for both host.

##### ACTUAL RESULTS

Playbook stops for host0, and continues to run the second task for host1 :

```
$ ansible-playbook playbook.yaml 

PLAY [all] ***************************************************************************************************************************************************************************************************************

TASK [Fail a single host] ************************************************************************************************************************************************************************************************
skipping: [host1]
fatal: [host0]: FAILED! => {"changed": false, "failed": true, "msg": "Failed as requested from task"}

TASK [Run on both host] **************************************************************************************************************************************************************************************************
ok: [host1] => {
    "msg": "Run on both host"
}

PLAY RECAP ***************************************************************************************************************************************************************************************************************
host0                      : ok=0    changed=0    unreachable=0    failed=1   
host1                      : ok=1    changed=0    unreachable=0    failed=0   
```

I ran a git bisect on the stable-2.4 branch to track down where the error cropped up.
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `f8230d961d4af427a9adbb8abf7b591b7d513f66` and the full history behind it is present.
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
