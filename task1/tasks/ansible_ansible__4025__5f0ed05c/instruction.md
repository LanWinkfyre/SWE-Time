# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Jinja template evaluation fails on undefined variables even when error_on_undefined_vars = False

I have some jinja templates that I make use of variables that may or may not be defined, but have Jinja if/elif statements that deal with this correctly. 





After this commit creation of the template fails with this error:

fatal: [127.0.0.1] => {'msg': "One or more undefined variables: 'dict' object has no attribute 'facts'", 'failed': True}
fatal: [127.0.0.1] => {'msg': "One or more undefined variables: 'dict' object has no attribute 'facts'", 'failed': True}

even when the "error_on_undefined_vars = False" is set in the ansible.cfg file.  Here is an example of such template:

``` jinja2
{% for nic in virtual_machine.vm_nic|dictsort %}
{% if nic[1].kickstart == "yes" %}
{% if loop.index0 == 0 %}
network --onboot yes --device=eth0 --bootproto=static --ip={{ eth0.facts.network_ipaddress }} --netmask={{ eth0.facts.network_netmask }} --gateway={{ eth0.facts.network_gateway }} --nameserver={{ eth0.facts.network_nameservers[0] }} --noipv6 --activate
{% elif loop.index0 == 1 %}
network --onboot yes --device=eth1 --bootproto=static --ip={{ eth1.facts.network_ipaddress }} --netmask={{ eth1.facts.network_netmask }} --gateway={{ eth1.facts.network_gateway }} --nameserver={{ eth1.facts.network_nameservers[0] }} --noipv6 --activate
{% elif loop.index0 == 2 %}
network --onboot yes --device=eth2 --bootproto=static --ip={{ eth2.facts.network_ipaddress }} --netmask={{ eth2.facts.network_netmask }} --gateway={{ eth2.facts.network_gateway }} --nameserver={{ eth2.facts.network_nameservers[0] }} --noipv6 --activate
{% endif %}
{% endif %}
{% endfor %}
```

Please let me know if you need any more information.
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `fff497a1aef6db7f2a8f92d981a6b9a789bf798e` and the full history behind it is present.
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
