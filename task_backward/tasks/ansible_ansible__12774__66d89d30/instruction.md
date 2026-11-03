# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
v1.9->2: templated delegate_to with undefined variable fails even if task is skipped on when: undefined

 This does not happen in 1.9.

Following task snippet reproduces this
(source: https://github.com/bennojoy/mysql/blob/master/tasks/main.yml#L85)

```
139 - name: Get the current master servers replication status                       
140   mysql_replication:                                                            
141     mode:   getmaster                                                           
142   delegate_to: "{{ mysql_repl_master }}"                                        
143   register: repl_stat                                                           
144   when: slave|failed and mysql_repl_role == 'slave' and mysql_repl_master is defined
```

This works fine in 1.9, and used to work in 2.0 (at least until some months/weeks ago).

```
TASK: [mysql | Get the current master servers replication status] ****** 
skipping: [hydargos]
```



```
TASK [mysql : Get the current master servers replication status] ********
fatal: [hydargos -> {{ mysql_repl_master }}]: FAILED! => {"failed": true, "msg": "ERROR! 'mysql_repl_master' is undefined"}
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `174ecb843c718ce70ec69cd575c36ce8e3f70ffb` and the full history behind it is present.
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
