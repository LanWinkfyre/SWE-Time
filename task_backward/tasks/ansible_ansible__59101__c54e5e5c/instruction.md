# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
gcp_compute incorrectly prints data to screen, breaking JSON output for ansible-inventory

<!--- Verify first that your issue is not already reported on GitHub -->
<!--- Also test if the latest release and devel branch are affected too -->
<!--- Complete *all* sections as described, this form is processed automatically -->

##### SUMMARY
<!--- Explain the problem briefly below -->
`ansible-inventory` is supposed to return JSON...
but it does not when installing anisble@devel, and running a GCE inventory update with this `gcp_compute.yml` to use the gcp inventory plugin:

```
auth_kind: serviceaccount
filters: null
plugin: gcp_compute
projects:
- myproject
service_account_file: creds.json
```

##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME
<!--- Write the short name of the module, plugin, task or feature below, use your best guess if unsure -->
gcp inventory plugin
##### ANSIBLE VERSION
<!--- Paste verbatim output from "ansible --version" between quotes -->
```paste below
 ansible-inventory --version    
ansible-inventory 2.9.0.dev0
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/elijah/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /home/elijah/venvs/py36towerqa/lib64/python3.6/site-packages/ansible 
  executable location = /home/elijah/venvs/py36towerqa/bin/ansible-inventory                            
  python version = 3.6.8 (default, Feb 19 2019, 21:10:40) [GCC 9.0.1 20190209 (Red Hat 9.0.1-0.4)] 
```

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
```paste below
#no output
```

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->


##### STEPS TO REPRODUCE
<!--- Describe exactly how to reproduce the problem, using a minimal test-case -->
1) Create gcp_comput.yml and creds.json to access your gcp account
2) Create python36 venv
3) install anisble@stable-2.8
4) run `ansible-inventory -i gcp_compute.yml --list > ouput.28`
5) Inspect the output, see that it is valid JSON.
6) install ansible@devel
4) run `ansible-inventory -i gcp_compute.yml --list > ouput.devel`
7) Inspect output, see that before the part that starts the JSON that looks like:
```
{
    "_meta": {
        "hostvars": {
```
there is a bug chunk of key/value pairs in a list:
```
[{'key': 'blahkey', 'value': 'blahvalue}, {'key': 'ssh-keys', 'value': 'somebody's key'} {'key': 'more keys', 'value': 'more values' ...... ] 
```


<!--- HINT: You can paste gist.github.com links for larger files -->

##### EXPECTED RESULTS
<!--- Describe what you expected to happen when running the steps above -->
JSON

##### ACTUAL RESULTS
<!--- Describe what actually happened. If possible run with extra verbosity (-vvvv) -->
List of key/value pairs then regular json ouput
<!--- Paste verbatim command output between quotes -->
```paste below

```
This is a tower blocker for the next release of ansible.
 (private repo) https://github.com/ansible/tower/issues/3605
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `262c9ffdb6c995d67a8dfd3707ec8bb09a4fd77d` and the full history behind it is present.
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
