# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
rhn_register module failing with 1.5.3 

##### Issue Type:

Bug Report
##### Ansible Version:

ansible 1.5.3
##### Environment:

Ansible 1.5.3 on OS X, running against CentOS 6.5 hosts managed by Spacewalk.
##### Summary:

Module rhn_register module stopped working for me in Ansible 1.5.3 on CentOS 6.5 hosts connecting to a Spacewalk server. Worked in 1.5.
##### Steps To Reproduce:

```
rhn_register: state=present activationkey={{ spacewalk_key }} server_url={{ spacewalk_url }}
```
##### Expected Results:

```
ok: [***host****] => {"changed": false, "item": "", "msg": "System already registered."}
```
##### Actual Results:

```
Traceback (most recent call last):
  File "/home/mpontes/.ansible/tmp/ansible-tmp-1395139130.65-131190767219818/rhn_register", line 88, in <module>
    class Rhn(RegistrationBase):
NameError: name 'RegistrationBase' is not defined
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `84908a57fce3e6c1919ab7b85839f40d7f7d9585` and the full history behind it is present.
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
