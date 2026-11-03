# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Role parameter: change in variable precedence

### Summary

Hi ; 

Since Ansible 8.0.0 (I think, I didn't check every ansible-core version), it seams that role parameters do not take precedence over already define facts.

According to the [documentation](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence), role (and include_role) params (line 20) should still take precedence over set_facts / registered vars (line 19). I also checked [Ansible 8.x changelogs](https://github.com/ansible-community/ansible-build-data/blob/main/8/CHANGELOG-v8.rst) but I didn't see anything about that, except maybe [this bug fix](https://github.com/ansible-community/ansible-build-data/blob/a8cf3895cd98246316ab6172ec684935e0013b45/8/CHANGELOG-v8.rst#L3397), I'm not sure what `Also adjusted the precedence to act the same as inline params` means and what are the expected impacts. But if this is a wanted new behavior, I feal like it should be details in major changes, not in the bug fix section.

### Issue Type

Bug Report

### Component Name

role

### Ansible Version

```console
ansible [core 2.15.2]
  config file = /home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg
  configured module search path = ['/home/courgette/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/courgette/.virtualenvs/deploy/lib/python3.11/site-packages/ansible
  ansible collection location = /home/courgette/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/courgette/.virtualenvs/deploy/bin/ansible
  python version = 3.11.3 (main, Jun  5 2023, 09:32:32) [GCC 13.1.1 20230429] (/home/courgette/.virtualenvs/deploy/bin/python)
  jinja version = 3.1.2
  libyaml = True
```


### Configuration

```console
CONFIG_FILE() = /home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg
DEFAULT_FILTER_PLUGIN_PATH(/home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg) = ['/home/courgette/Documents/Bimdata/dev/deployment/ansible_plugins/filter_plugins']
DEFAULT_TIMEOUT(/home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg) = 60
DEFAULT_VAULT_PASSWORD_FILE(/home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg) = /home/courgette/Documents/Bimdata/dev/deployment/.get-vault-pass.sh
EDITOR(env: EDITOR) = vim
PAGER(env: PAGER) = less

CONNECTION:
==========

paramiko_ssh:
____________
timeout(/home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg) = 60

ssh:
___
pipelining(/home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg) = True
timeout(/home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg) = 60
```


### OS / Environment

Tested on Archlinux and also in python:3.11 docker container. 

### Steps to Reproduce

Create `roles/test_set/tasks/main.yml` with:

```
---
- name: "Set test fact."
  ansible.builtin.set_fact:
    test_set_one: "set by test_set"
```

Create `roles/test_debug/tasks/main.yml` with:
```
---
- name: "Debug the variable."
  ansible.builtin.debug:
    var: test_set_one

```

Create `test.yml` with:
 ```
---
- name: Test
  hosts: localhost
  gather_facts: false
  become: false
  roles:
    - test_set
    - test_debug
    - role: test_debug
      test_set_one: "Set as role parameter"
```

Run: `ansible-playbook test.yml`.

### Expected Results

```
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Test] *********************************************************************************************************************************************************************************************************

TASK [test_set : Set test fact.] ************************************************************************************************************************************************************************************
ok: [localhost]

TASK [test_debug : Debug the variable.] *****************************************************************************************************************************************************************************
ok: [localhost] => {
    "test_set_one": "set by test_set"
}

TASK [test_debug : Debug the variable.] *****************************************************************************************************************************************************************************
ok: [localhost] => {
    "test_set_one": "Set as role parameter"
}

PLAY RECAP **********************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```

This is a the result with ansible 7.x, here the corresponding version used to obtain it: 
```
ansible [core 2.14.8]
  config file = /home/courgette/Documents/Bimdata/dev/deployment/ansible.cfg
  configured module search path = ['/home/courgette/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/courgette/.virtualenvs/deploy/lib/python3.11/site-packages/ansible
  ansible collection location = /home/courgette/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/courgette/.virtualenvs/deploy/bin/ansible
  python version = 3.11.3 (main, Jun  5 2023, 09:32:32) [GCC 13.1.1 20230429] (/home/courgette/.virtualenvs/deploy/bin/python)
  jinja version = 3.1.2
  libyaml = True
```

### Actual Results

```console
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Test] *********************************************************************************************************************************************************************************************************

TASK [test_set : Set test fact.] ************************************************************************************************************************************************************************************
ok: [localhost]

TASK [test_debug : Debug the variable.] *****************************************************************************************************************************************************************************
ok: [localhost] => {
    "test_set_one": "set by test_set"
}

TASK [test_debug : Debug the variable.] *****************************************************************************************************************************************************************************
ok: [localhost] => {
    "test_set_one": "set by test_set"
}

PLAY RECAP **********************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `fa5fe8a7db51cc5ff62689780db5296821708a19` and the full history behind it is present.
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
