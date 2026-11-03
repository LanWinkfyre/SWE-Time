# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
get_url incorrectly returning a 302 error

##### Issue Type:
- Bug Report
##### Ansible Version:


##### Environment:

running from OS X El Capitan
controlling CentOS
##### Summary:

Getting a 302 error trying to download rpm. The rpm is there.
##### Steps To Reproduce:

<!---
For bugs, please show exactly how to reproduce the problem. For new
features, show how the feature would be used.
-->

```
vars/rmpforge.yml:

---
rpmforge_version: 0.5.3-1.el6.rf.x86_64

install_rpmforge.yml:

---
- include_vars: vars/rpmforge.yml

- name: get rpmforge
  get_url:
    url: 'http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-{{ rpmforge_version }}.rpm'
    dest: /usr/src
    force: no


```
##### Expected Results:

If the file exists locally, I expect it to not do much at all
If the file doesn't exist locally, I expect it to get it
##### Actual Results:

Get a 302 error in either case

```
TASK [get rpmforge] ************************************************************
fatal: [trac]: FAILED! => {"changed": false, "dest": "/usr/src", "failed": true, "gid": 0, "group": "root", "mode": "0755", "msg": "Request failed", "owner": "root", "response": "HTTP Error 302: Found", "secontext": "system_u:object_r:usr_t:s0", "size": 4096, "state": "directory", "status_code": 302, "uid": 0, "url": "http://pkgs.repoforge.org/rpmforge-release/rpmforge-release-0.5.3-1.el6.rf.x86_64.rpm"}
    to retry, use: --limit @install_utilities.retry

```


I hit this same bug.  Using `git bisect` I tracked down the problematic commit, which is prior to the version indicated by @jgrigonis. 



FYI @sivel
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `347aa7b0328699b33cf8d435511b42285bf87da7` and the full history behind it is present.
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
