# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
set_fact behavior has changed with ansible release 2.12.1

### Summary

Different ansible versions have different 'set_fact' behaviors.

### Issue Type

Bug Report

### Component Name

set_fact

### Ansible Version

```console
## Newest version on fedora 34
$ ansible --version
ansible [core 2.12.1]
  config file = None
  configured module search path = ['/home/plewyllie/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/plewyllie/.local/lib/python3.9/site-packages/ansible
  ansible collection location = /home/plewyllie/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/plewyllie/.local/bin/ansible
  python version = 3.9.9 (main, Nov 19 2021, 00:00:00) [GCC 11.2.1 20210728 (Red Hat 11.2.1-1)]
  jinja version = 2.11.3
  libyaml = True

## Working version (on mac os x)
ansible [core 2.11.6]
  config file = None
  configured module search path = ['/Users/plewyllie/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/Cellar/ansible/4.8.0/libexec/lib/python3.10/site-packages/ansible
  ansible collection location = /Users/plewyllie/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.10.0 (default, Oct 13 2021, 06:45:00) [Clang 13.0.0 (clang-1300.0.29.3)]
  jinja version = 3.0.2
  libyaml = True
```


### Configuration

```console
$ ansible-config dump --only-changed
```


### OS / Environment

Fedora. I used Mac OS X to confirm the 'older' behavior to avoid a downgrade process. However, the previous version that I had on Fedora was working in the same way, it's updating ansible that has caused this issue to appear.

### Steps to Reproduce

<!--- Paste example playbooks or commands between quotes below -->
### Test Playbook
```
---
## Naming VMs for OCP
## Each VM going through this list should have the new fact "vm_name" set to "cluster_name"-"initial_vm_name"
- hosts: localhost
  gather_facts: no
  tasks:
  - set_fact:
      vm_name : "{{ cluster_name }}-{{ hostvars[item].inventory_hostname }}"
    delegate_to: "{{ item }}"
    delegate_facts: True
    with_items: "{{ groups['vms'] }}"

  - debug:
      msg: "{{ item }} vm_name  {{ hostvars[item].vm_name }}"
    with_items: "{{ groups['vms'] }}"
```

### Test inventory
```
[vms]
install
lb

[all:vars]
cluster_name=ocp4-pieter
```

### Expected Results


With ansible [core 2.11.6] the output will be:
```
TASK [debug] *************************************************************************************************************
ok: [localhost] => (item=install) => {
    "msg": "install vm_name  ocp4-pieter-install"
}
ok: [localhost] => (item=lb) => {
    "msg": "lb vm_name  ocp4-pieter-lb"
}
```

With the newer ansible [core 2.12.1] the output looks like this:
```
TASK [debug] *************************************************************************************************************************
ok: [localhost] => (item=install) => {
    "msg": "install vm_name  ocp4-pieter-lb"
}
ok: [localhost] => (item=lb) => {
    "msg": "lb vm_name  ocp4-pieter-lb"
}
```

I have also tried with the development branch:


### Actual Results

```console
TASK [debug] *************************************************************************************************************************
ok: [localhost] => (item=install) => {
    "msg": "install vm_name  ocp4-pieter-lb"
}
ok: [localhost] => (item=lb) => {
    "msg": "lb vm_name  ocp4-pieter-lb"
}
```


### Code of Conduct

- [X] I agree to follow the Ansible Code of Conduct
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `b984dd9c59dd43d50f5aafa91cfde29405f2fbd9` and the full history behind it is present.
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
