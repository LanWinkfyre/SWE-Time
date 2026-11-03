# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Sudo/Become doesnt work on local connection in loops

I am having a confusing problem. It does look like a bug and hence I am reporting here, not sure if duplicate.

I am using ansible version 2.0.0 locally on OSX El Capitan, to run a series of steps which sets up my machine for development for my project. The last step here is to add a few lines to `/etc/hosts` (~15 lines)
I am using `lineinfile` to add these lines in a loop. 

I have tried `become: root` with `become_ask_pass=True` in the cfg file. This does nothing. It does not ask my password and once it hits that task, I get `The destination directory (/private/etc) is not writable by the current user.`. If I try `sudo: yes` and `ask_sudo_pass=True` then I get `fatal: [localhost]: FAILED! => {"failed": true, "msg": "ERROR! privilege output closed while waiting for password prompt:\nBECOME-SUCCESS-jpibjiakmfjdrjafspqizphqotvhjikm\n{\"msg\": \"line added\", \"changed\": true, \"backup\": \"\"}\n"}`. But infact If i check now, `/etc/hosts` file now has the first 2 lines of the list of lines I had to add. Running the playbook now doesnt help me at all.. but even more oddly, If i remove the config option to ask for password and run the play it works fully.... 


Confirming the error with `become: True` and a local connection. The other factor I see is that `-K` parameter has been used to request a password - without the `-K` parameter, but after `sudo` has been "primed" by the user giving the password, Ansible works fine. Here's an example playbook I used for testing:

```
---
- hosts: all
  become: True

  tasks:
    - name: Make sure required directories exist
      file:
        path: '{{ item }}'
        state: 'directory'
      with_items: [ '/bin', '/etc' ]
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `45355cd5660da17350811d92a5144077910ea434` and the full history behind it is present.
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
