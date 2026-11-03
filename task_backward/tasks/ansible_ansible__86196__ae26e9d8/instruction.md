# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[2.19 regression] Type 'timedelta' is unsupported for variable storage

### Summary

Since ansible-core 2.19.0, I haven't been able to store variables of type `timedelta`.  

### Issue Type

Bug Report

### Component Name

python timedelta

### Ansible Version

```console
$ ansible --version
ansible [core 2.19.0.dev0]
  config file = /home/mconway/.ansible.cfg
  configured module search path = ['/home/mconway/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.13/site-packages/ansible
  ansible collection location = /home/mconway/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/lib/python-exec/python3.13/ansible
  python version = 3.13.5 (main, Jul 31 2025, 13:33:30) [GCC 14.3.0] (/usr/bin/python3.13)
  jinja version = 3.1.6
  libyaml = True
```

### Configuration

```console
$ ansible-config dump --only-changed -t all
ANSIBLE_PIPELINING(/home/mconway/.ansible.cfg) = True
CONFIG_FILE() = /home/mconway/.ansible.cfg
DEFAULT_FORKS(/home/mconway/.ansible.cfg) = 25
EDITOR(env: EDITOR) = vi
PAGER(env: PAGER) = /usr/bin/less

GALAXY_SERVERS:


CONNECTION:
==========

local:
_____
pipelining(/home/mconway/.ansible.cfg) = True

paramiko_ssh:
____________
pty(/home/mconway/.ansible.cfg) = False

psrp:
____
pipelining(/home/mconway/.ansible.cfg) = True

ssh:
___
pipelining(/home/mconway/.ansible.cfg) = True
ssh_args(/home/mconway/.ansible.cfg) = -o ControlMaster=auto -o ControlPersist=2m

winrm:
_____
pipelining(/home/mconway/.ansible.cfg) = True
```

### OS / Environment

Gentoo

### Steps to Reproduce

```yaml
---
- name: Ansible timedelta test
  hosts: localhost
  gather_facts: false
  vars:
    expires: 2026-06-02 15:20:35
  tasks:
    - name: Debug timedelta
      loop:
        - expires
        - expires - now()
      ansible.builtin.debug:
        var: '{{ item }}'
```

### Expected Results

```
PLAY [Ansible timedelta test] ********************************************************************

TASK [Debug variables] ***************************************************************************
ok: [localhost] => (item=expires) => {
    "expires": "2026-06-02 15:20:35",
    "item": "expires"
}
ok: [localhost] => (item=expires - now()) => {
    "expires - now()": "201 days, 3:13:44.391734",
    "item": "expires - now()"
}

PLAY RECAP ***************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

### Actual Results



### Code of Conduct

- [x] I agree to follow the Ansible Code of Conduct
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `69c9fbed26543bb3a998c2b0d0a76db05358febf` and the full history behind it is present.
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
