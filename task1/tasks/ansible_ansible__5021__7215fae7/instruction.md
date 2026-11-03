# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
authorized_keys module traceback when quote present in comment

Using a git checkout, and using this playbook:

```
#file sshkeys.yaml
- hosts:
    - other
  #sudo: yes
  tasks:
    - name: Add authorized keys
      authorized_key: key="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAwkgav3IMA1BdcM3QFFp5DfBakQlpwqxGujObR9okU32qmNbOdDn8kYGhK7UAdUm1Kn+Jb+eVjy2db34s3Pyoym6/3ihGPSGaWA+n5SDeiMs6rzn2wBq+zhz83qzVpMs/NUl1kFSbFLSXYXJ/u/hrnsIaoghQyRLT0eBWY3ja8ZsI0g4tTrAtDez+ovcn0d/50K3k+Y1QJxFuys8cvNh7YC3WHCgU0jm32HZa3EHTEYqmsbS0dhLrmDl05b8sNTfWHKTcDOVo6wAHwee0I+eb1SMOFt2RmMS6y+R0bCqy32F4Ix7xVKRI2KOc1XKctu2Nl9yLadCM9TeGGCMpP90Dnw== jtate@laputa" state=present user=root
      tags: [deploy,ssh]
```

I'm getting the following error:

```
$ ansible-playbook -i inventories/other2 -vvvv sshkeys.yml 

PLAY [other] ****************************************************************** 

GATHERING FACTS *************************************************************** 
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> ESTABLISH CONNECTION FOR USER: root
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> EXEC ['ssh', '-tt', '-vvv', '-o', 'ControlMaster=auto', '-o', 'ControlPersist=60s', '-o', 'ControlPath=/home/jtate/.ansible/cp/ansible-ssh-%h-%p-%r', '-o', 'Port=22', '-o', 'KbdInteractiveAuthentication=no', '-o', 'PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey', '-o', 'PasswordAuthentication=no', '-o', 'User=root', '-o', 'ConnectTimeout=10', 'ec2-54-245-205-210.us-west-2.compute.amazonaws.com', "/bin/sh -c 'mkdir -p $HOME/.ansible/tmp/ansible-1385152217.14-277861042071907 && chmod a+rx $HOME/.ansible/tmp/ansible-1385152217.14-277861042071907 && echo $HOME/.ansible/tmp/ansible-1385152217.14-277861042071907'"]
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> REMOTE_MODULE setup 
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> PUT /tmp/tmptXH14h TO /root/.ansible/tmp/ansible-1385152217.14-277861042071907/setup
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> EXEC ['ssh', '-tt', '-vvv', '-o', 'ControlMaster=auto', '-o', 'ControlPersist=60s', '-o', 'ControlPath=/home/jtate/.ansible/cp/ansible-ssh-%h-%p-%r', '-o', 'Port=22', '-o', 'KbdInteractiveAuthentication=no', '-o', 'PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey', '-o', 'PasswordAuthentication=no', '-o', 'User=root', '-o', 'ConnectTimeout=10', 'ec2-54-245-205-210.us-west-2.compute.amazonaws.com', "/bin/sh -c '/usr/bin/python /root/.ansible/tmp/ansible-1385152217.14-277861042071907/setup; rm -rf /root/.ansible/tmp/ansible-1385152217.14-277861042071907/ >/dev/null 2>&1'"]
ok: [ec2-54-245-205-210.us-west-2.compute.amazonaws.com]

TASK: [Add authorized keys] *************************************************** 
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> ESTABLISH CONNECTION FOR USER: root
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> EXEC ['ssh', '-tt', '-vvv', '-o', 'ControlMaster=auto', '-o', 'ControlPersist=60s', '-o', 'ControlPath=/home/jtate/.ansible/cp/ansible-ssh-%h-%p-%r', '-o', 'Port=22', '-o', 'KbdInteractiveAuthentication=no', '-o', 'PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey', '-o', 'PasswordAuthentication=no', '-o', 'User=root', '-o', 'ConnectTimeout=10', 'ec2-54-245-205-210.us-west-2.compute.amazonaws.com', "/bin/sh -c 'mkdir -p $HOME/.ansible/tmp/ansible-1385152224.84-190783874081238 && chmod a+rx $HOME/.ansible/tmp/ansible-1385152224.84-190783874081238 && echo $HOME/.ansible/tmp/ansible-1385152224.84-190783874081238'"]
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> REMOTE_MODULE authorized_key key="ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAwkgav3IMA1BdcM3QFFp5DfBakQlpwqxGujObR9okU32qmNbOdDn8kYGhK7UAdUm1Kn+Jb+eVjy2db34s3Pyoym6/3ihGPSGaWA+n5SDeiMs6rzn2wBq+zhz83qzVpMs/NUl1kFSbFLSXYXJ/u/hrnsIaoghQyRLT0eBWY3ja8ZsI0g4tTrAtDez+ovcn0d/50K3k+Y1QJxFuys8cvNh7YC3WHCgU0jm32HZa3EHTEYqmsbS0dhLrmDl05b8sNTfWHKTcDOVo6wAHwee0I+eb1SMOFt2RmMS6y+R0bCqy32F4Ix7xVKRI2KOc1XKctu2Nl9yLadCM9TeGGCMpP90Dnw== jtate@laputa" state=present user=root
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> PUT /tmp/tmp4ACNxZ TO /root/.ansible/tmp/ansible-1385152224.84-190783874081238/authorized_key
<ec2-54-245-205-210.us-west-2.compute.amazonaws.com> EXEC ['ssh', '-tt', '-vvv', '-o', 'ControlMaster=auto', '-o', 'ControlPersist=60s', '-o', 'ControlPath=/home/jtate/.ansible/cp/ansible-ssh-%h-%p-%r', '-o', 'Port=22', '-o', 'KbdInteractiveAuthentication=no', '-o', 'PreferredAuthentications=gssapi-with-mic,gssapi-keyex,hostbased,publickey', '-o', 'PasswordAuthentication=no', '-o', 'User=root', '-o', 'ConnectTimeout=10', 'ec2-54-245-205-210.us-west-2.compute.amazonaws.com', "/bin/sh -c '/usr/bin/python /root/.ansible/tmp/ansible-1385152224.84-190783874081238/authorized_key; rm -rf /root/.ansible/tmp/ansible-1385152224.84-190783874081238/ >/dev/null 2>&1'"]
fatal: [ec2-54-245-205-210.us-west-2.compute.amazonaws.com] => failed to parse: Traceback (most recent call last):
  File "/root/.ansible/tmp/ansible-1385152224.84-190783874081238/authorized_key", line 1397, in <module>
    main()
  File "/root/.ansible/tmp/ansible-1385152224.84-190783874081238/authorized_key", line 368, in main
    results = enforce_state(module, module.params)
  File "/root/.ansible/tmp/ansible-1385152224.84-190783874081238/authorized_key", line 302, in enforce_state
    existing_keys = readkeys(params["keyfile"])
  File "/root/.ansible/tmp/ansible-1385152224.84-190783874081238/authorized_key", line 246, in readkeys
    key_data = parsekey(line)
  File "/root/.ansible/tmp/ansible-1385152224.84-190783874081238/authorized_key", line 212, in parsekey
    key_parts = shlex.split(raw_key)
  File "/usr/lib/python2.7/shlex.py", line 279, in split
    return list(lex)
  File "/usr/lib/python2.7/shlex.py", line 269, in next
    token = self.get_token()
  File "/usr/lib/python2.7/shlex.py", line 96, in get_token
    raw = self.read_token()
  File "/usr/lib/python2.7/shlex.py", line 172, in read_token
    raise ValueError, "No closing quotation"
ValueError: No closing quotation


FATAL: all hosts have already failed -- aborting

PLAY RECAP ******************************************************************** 
           to retry, use: --limit @/home/jtate/sshkeys.retry

ec2-54-245-205-210.us-west-2.compute.amazonaws.com : ok=1    changed=0    unreachable=1    failed=0   

```


Git bisect tells me that it stopped working on




Ahh. My EC2 key has a single ' in it:

ssh-rsa AAAAB.....== jtate's key
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `815b32685b377a9cc07c7a6f06bb080025b174fe` and the full history behind it is present.
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
