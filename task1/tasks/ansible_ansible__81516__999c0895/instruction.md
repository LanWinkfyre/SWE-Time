# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ansible.builtin.pause consumes whole CPU core while waiting

### Summary

ansible.builtin.pause consumes whole CPU core while waiting



As a workaround one can use `ansible.builtin.wait_for`. It does not load CPU now:

```yaml
- name: Sleep for 300 seconds and continue with play
  ansible.builtin.wait_for:
    timeout: 300
  delegate_to: localhost
```

### Issue Type

Bug Report

### Component Name

ansible.builtin.pause

### Ansible Version

```console
$ ansible --version
ansible [core 2.15.2]
  config file = /home/self/.ansible.cfg
  configured module search path = ['/home/self/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/self/.local/lib/python3.10/site-packages/ansible
  ansible collection location = /home/self/.ansible/collections:/usr/share/ansible/collections
  executable location = /home/self/.local/bin/ansible
  python version = 3.10.12 (main, Jun 11 2023, 05:26:28) [GCC 11.4.0] (/usr/bin/python3)
  jinja version = 3.0.3
  libyaml = True
```


### Configuration

```console
$ ansible-config dump --only-changed -t all
CONFIG_FILE() = /home/self/.ansible.cfg
EDITOR(env: EDITOR) = vim

CONNECTION:
==========

ssh:
___
pipelining(/home/self/.ansible.cfg) = True
```


### OS / Environment

Arch, Ubuntu

### Steps to Reproduce

<!--- Paste example playbooks or commands between quotes below -->
```yaml (paste below)
- hosts: localhost
  gather_facts: no

  tasks:
    - name: Pause for 5 second
      ansible.builtin.pause:
        seconds: 5
```


### Expected Results

I expect to CPU be mostly idle while the task is waiting for timeout.

### Actual Results

```console
$ time ansible-playbook -i '/dev/null' benchmark_pause.yaml                                                                                           
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [localhost] ********************************************************************************************************************************************************

TASK [Pause for 5 second] ***********************************************************************************************************************************************
Pausing for 5 seconds
(ctrl+C then 'C' = continue early, ctrl+C then 'A' = abort)
ok: [localhost]

PLAY RECAP **************************************************************************************************************************************************************
localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0


real    0m5,892s
user    0m2,784s
sys     0m3,171s
```

Note that user+system time is 5 seconds.
```


### Code of Conduct

- [X] I agree to follow the Ansible Code of Conduct
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `bd3ffbe10903125993d7d68fa8cfd687124a241f` and the full history behind it is present.
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
