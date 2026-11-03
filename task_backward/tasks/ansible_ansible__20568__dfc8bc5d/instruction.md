# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Regression in Ansible 2.2 using raw / endraw jinja tags and GO templates.

##### ISSUE TYPE
<!--- Pick one below and delete the rest: -->
 - Bug Report

##### COMPONENT NAME
<!--- Name of the module/plugin/task/feature -->
shell module with {% raw %} tags

##### ANSIBLE VERSION
<!--- Paste verbatim output from “ansible --version” between quotes below -->
```
ansible 2.2.1.0
  config file = /etc/ansible/ansible.cfg
  configured module search path = Default w/o overrides
```

##### CONFIGURATION
N/A

##### OS / ENVIRONMENT
N/A (CentOS 7.2 shouldn't be platform specific)

##### SUMMARY
<!--- Explain the problem briefly -->
This is quite meta .. but I will try and explain.

We use the ansible shell command to run some commands against docker hosts which uses dockers --format feature that feature relies on GO template engine. Naturally we see conflicting behaviour here due to both jinja2 and go using '{{' as delimeters. AFAIK neither of these tools currently support switching delimeters but I may be wrong as that would be one way we could work around this..

We pass a {% raw %}{% endraw %} wrapped go template to a shell module calling docker like:
```
  - name: Count running images to check if down scaling is necessary
    shell:
      "docker ps -a --no-trunc --filter name=^/{{artifact.namespace}}-{{ artifact.name }} --format='{% raw %}{{.ID}},{{.Image}}{% endraw %}' | wc -l"
    register: docker_container_count

  - name: Debug the count
    debug:
      msg: "{{ docker_container_count }}" 
```
The command executes successfully in both Ansible 2.1.1.0 and Ansible 2.2.1.0 
**however**
The internal representation 'cmd' key representing the original command was stored using the jinja tags as '{#'  and now it is being stored verbatim like '{{'. This is causing any further usage of this registered variable to fail as jinja is trying to parse the 'cmd' string.

debug output before upgrade (v2.1.1.0):
```
16:33:28 TASK [microservices : Debug the count] *************************
16:33:28 ok: [hostname.company.org] => {
16:33:28     "msg": {
16:33:28         "changed": true, 
16:33:28         "cmd": "docker ps -a --no-trunc --filter name=^/edge-server--account-service --format='{#.ID#},{#.Image#}' | wc -l", 
16:33:28         "delta": "0:00:00.025972", 
16:33:28         "end": "2017-01-23 16:33:27.970780", 
16:33:28         "rc": 0, 
16:33:28         "start": "2017-01-23 16:33:27.944808", 
16:33:28         "stderr": "", 
16:33:28         "stdout": "1", 
16:33:28         "stdout_lines": [
16:33:28             "1"
16:33:28         ], 
16:33:28         "warnings": []
16:33:28     }
16:33:28 }
16:33:28 
```
debug output after upgrade (v2.2.1.0):
```
16:07:24 TASK [microservices : Debug the count] ***********************************
16:07:24 fatal: [hostname.company.org]: FAILED! => 
{"failed": true, 
   "msg": "{
     u'cmd': u\"docker ps -a --no-trunc --filter name=^/edge-server--account-service --format='{{.ID}},{{.Image}}' | wc -l\", 
     u'end': u'2017-01-23 16:07:24.798553', 
     u'stdout': u'1', 
     u'changed': True, 
     u'start': u'2017-01-23 16:07:24.763174', 
     u'delta': u'0:00:00.035379', 
     u'stderr': u'', 
     u'rc': 0, 
     'stdout_lines': [u'1'], 
     u'warnings': []}: 
  template error while templating string: unexpected '.'. String: docker ps -a --no-trunc --filter name=^/edge-server--account-service --format='{{.ID}},{{.Image}}' | wc -l"
}
16:07:24 	to retry, use: --limit @/home/jenkins/workspace/DeploymentFolder/DeployEdgeServer/rolling_deployment.retry
16:07:24 
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `43519c9bef1ecf0dd4a3d0839578e04c85e90a1d` and the full history behind it is present.
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
