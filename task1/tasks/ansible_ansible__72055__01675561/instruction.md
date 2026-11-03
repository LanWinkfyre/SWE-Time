# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
blockinfile in 2.10 is not adding a newline at the start of the block

<!--- Verify first that your issue is not already reported on GitHub -->
<!--- Also test if the latest release and devel branch are affected too -->
<!--- Complete *all* sections as described, this form is processed automatically -->

##### SUMMARY

`blockinfile` in Ansible 2.10 seems to behave differently than it did on 2.9.

Previously, when adding a block it seemed to start on a new line, now it is appended to the last line.

I think this is a bug for two reasons:

* It's a breaking change and didn't see it anywhere (apologies if I've missed it).
* It breaks idempotency, as a second run will add the block again.

It's also worth noting that 2.9 didn't seem to add a newline at the end of the block, while 2.10 does.

##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME
<!--- Write the short name of the module, plugin, task or feature below, use your best guess if unsure -->
blockinfile

##### ANSIBLE VERSION
<!--- Paste verbatim output from "ansible --version" between quotes -->
```paste below
ansible 2.10.1
  config file = None
  configured module search path = ['/home/hector/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/hector/.local/lib/python3.8/site-packages/ansible
  executable location = /home/hector/.local/bin/ansible
  python version = 3.8.2 (default, Jul 16 2020, 14:00:26) [GCC 9.3.0]

```

Works fine on 2.9.13

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
```paste below

```

I'm using the default Ansible configuration.

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->

Tested on:

* Ubuntu 18 and 20
* CentOS 6, 7 and 8
* Debian 8, 9 and 10

##### STEPS TO REPRODUCE

The following playbook reproduces the issue. Simply run it and it will create a local file, add some content into it which doesn't end in a newline and then it will add a block to it.

<!--- Paste example playbooks or commands between quotes below -->
```yaml
---

- name: 'blockinfile bug demonstration'
  hosts: localhost
  connection: local
  vars:
    _test_file: '/tmp/test'
  tasks:
    - name: 'Copy some contents on a file'
      copy:
        dest: "{{ _test_file }}"
        content: '# This is a test file'
        mode: '0600'
        force: false

    - name: 'Add a block to the file'
      blockinfile:
        path: "{{ _test_file }}"
        marker: "# {mark} First block"
        block: |
          # This is the first line of the block
          # This is the second line of the block

```

If the playbook is ran twice it will report changes because the block doesn't start in a new line and thus the module will think that the block is not present.

If it is ran thrice or more times then it will be idempotent, but the resulting file witll have two blocks added instead of one.

<!--- HINT: You can paste gist.github.com links for larger files -->

##### EXPECTED RESULTS

<!--- Describe what you expected to happen when running the steps above -->

The end result file is expected to be like this, which is the result that Ansible 2.9.13 had (note that I'm using `cat -E` which shows newlines with the character `$`):

```
cat -E /tmp/test
# This is a test file$
# BEGIN First block$
# This is the first line of the block$
# This is the second line of the block$
# END First block
```

All subsequent runs are expected to be idempotent and not modify the file at all.

Note that the block **doesn't** end in a newline.

##### ACTUAL RESULTS

The first run ends out with a file such as this one:

```
cat -E /tmp/test
# This is a test file# BEGIN First block$
# This is the first line of the block$
# This is the second line of the block$
# END First block$
```

A second run is _not_ idempotent and modifies the file again, ending with this content:


```
cat -E /tmp/test
# This is a test file# BEGIN First block$
# This is the first line of the block$
# This is the second line of the block$
# END First block$
# BEGIN First block$
# This is the first line of the block$
# This is the second line of the block$
# END First block$
```

Note that the block is inserted twice and it **does end** on a newline in both cases.

The output of three playbook runs is in this gist:

https://gist.githubusercontent.com/hluaces/9ea208b4123d6eeb70866515286988a3/raw/f8965cda67cd008a40ffc6ecde9b0ab4842982a8/output.txt
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `672df07a338b48d10440163ac815ceec14f0c2d3` and the full history behind it is present.
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
