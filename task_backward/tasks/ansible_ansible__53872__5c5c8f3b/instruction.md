# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Directly runnig module doesn't work with fetch_url() function within module

<!--- Verify first that your issue is not already reported on GitHub -->
<!--- Also test if the latest release and devel branch are affected too -->
<!--- Complete *all* sections as described, this form is processed automatically -->

##### SUMMARY
<!--- Explain the problem briefly below -->
I'm trying to run my module locally using next instructions https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#exercising-module-code-locally

And I get an error.

##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME
<!--- Write the short name of the module, plugin, task or feature below, use your best guess if unsure -->
Any module containing fetch_url() function from ansible.module_utils.urls
In my case it is my module I'm developing https://github.com/okgolove/ansible/blob/sentry_fixes/lib/ansible/modules/web_infrastructure/sentry_project.py

##### ANSIBLE VERSION
<!--- Paste verbatim output from "ansible --version" between quotes -->
```paste below
ansible 2.8.0.dev0
  config file = None
  configured module search path = [u'/Users/user/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/user/git/ansible/lib/ansible
  executable location = /Users/user/git/ansible/bin/ansible
  python version = 2.7.15 (default, Oct  2 2018, 11:47:18) [GCC 4.2.1 Compatible Apple LLVM 10.0.0 (clang-1000.11.45.2)]
```

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
args.json
```paste below
{
    "ANSIBLE_MODULE_ARGS": {
        "api_token": "abcxdz",
        "organization": "develop",
        "project_name": "backendtest",
        "project_slug": "backendtest",
        "state": "present",
        "team": "develop",
        "url": "https://sentry.io"
    }
}
```

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->
MacOS 10.14.3, Python 2.7.15

##### STEPS TO REPRODUCE
<!--- Describe exactly how to reproduce the problem, using a minimal test-case -->
```pipenv shell && source hacking/env-setup && python lib/ansible/modules/web_infrastructure/sentry_project.py args.json```

<!--- HINT: You can paste gist.github.com links for larger files -->

##### EXPECTED RESULTS
<!--- Describe what you expected to happen when running the steps above -->
Module runs properly.

##### ACTUAL RESULTS
<!--- Describe what actually happened. If possible run with extra verbosity (-vvvv) -->
And I get an error:

```Traceback (most recent call last):
  File "lib/ansible/modules/web_infrastructure/sentry_project.py", line 159, in <module>
    main()
  File "lib/ansible/modules/web_infrastructure/sentry_project.py", line 118, in main
    if is_project_exists(project_name, organization, team, api_token):
  File "lib/ansible/modules/web_infrastructure/sentry_project.py", line 110, in is_project_exists
    method="GET")
  File "/Users/user/git/ansible/lib/ansible/module_utils/urls.py", line 1327, in fetch_url
    tempfile.tempdir = module.tmpdir
  File "/Users/user/git/ansible/lib/ansible/module_utils/basic.py", line 851, in tmpdir
    basedir = os.path.expanduser(os.path.expandvars(self._remote_tmp))
AttributeError: 'AnsibleModule' object has no attribute '_remote_tmp'
```


This has not worked since Ansible 2.5.0.
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `906427cabac133d3690aff2225d33ef0dd34bcd5` and the full history behind it is present.
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
