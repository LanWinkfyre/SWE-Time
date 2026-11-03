# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Memory load increased in 2.3.0 compared to 2.2.0.1 (high memory use, high ram use)

##### ISSUE TYPE
 - Bug Report

##### COMPONENT NAME
Ansible

##### ANSIBLE VERSION
```
2.3.0
```

##### CONFIGURATION
```
[defaults]
hostfile       = inventory/
library        = /usr/share/ansible
remote_tmp     = $HOME/.ansible/tmp
pattern        = *
forks          = 30
poll_interval  = 15
sudo_user      = root
ask_sudo_pass  = True
transport      = ssh
remote_port    = 22
module_lang    = C
allow_world_readable_tmpfiles = True
gathering = implicit
host_key_checking = False
stdout_callback = actionable_debug
sudo_exe = sudo
sudo_flags = -i
timeout = 15
ansible_managed = This file is managed by Ansible.
action_plugins     = /usr/share/ansible_plugins/action_plugins
callback_plugins   = /usr/share/ansible_plugins/callback_plugins:./callback_plugins
connection_plugins = /usr/share/ansible_plugins/connection_plugins
lookup_plugins     = /usr/share/ansible_plugins/lookup_plugins
vars_plugins       = /usr/share/ansible_plugins/vars_plugins
filter_plugins     = /usr/share/ansible_plugins/filter_plugins
fact_caching = jsonfile
fact_caching_connection = /tmp/$USER
retry_files_enabled = False

[privilege_escalation]

[paramiko_connection]

[ssh_connection]
retries=10
pipelining = False

[accelerate]

[selinux]

[colors]
```

##### OS / ENVIRONMENT
Ubuntu 14.04.5 (exclusively) hosts & clients

##### SUMMARY
Increased memory usage when 2.3.0 is rolled out: http://imgur.com/a/ZgUCe



##### STEPS TO REPRODUCE

- Install Ansible 2.3.0
- Run regular job schedule (6x a day a full run of ~100 roles, several irregular jobs like backups), started from the Rundeck job scheduler over regular SSH.

##### EXPECTED RESULTS
Similar memory usage.

##### ACTUAL RESULTS
http://imgur.com/a/ZgUCe





I think that was actually our first suspect when this issue popped up but we couldn't reproduce at the time.   

pinging @jimi-c
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `f0f20d8a1c593005627250f17c0401df13ac26c0` and the full history behind it is present.
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
