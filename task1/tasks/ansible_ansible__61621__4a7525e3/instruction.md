# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ImportError: No module named json 

### SUMMARY

In the past week, my builds for my `geerlingguy.k8s` collection have started failing, both on Travis CI and locally. The failure message contains:

```
    TASK [Test k8s_template module.] ***********************************************
895    An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ModuleNotFoundError: No module named 'ansible.module_utils.common.json'
```

^ That was on Travis CI, locally with latest devel today I get:

```
    TASK [Test k8s_template module.] ***********************************************
    An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ImportError: No module named json
```

I did a `git bisect` and tracked it down to:



##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME

json module

##### ANSIBLE VERSION

```paste below
ansible 2.9.0.dev0
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/Users/jgeerling/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/jgeerling/Downloads/ansible/lib/ansible
  executable location = /Users/jgeerling/Downloads/ansible/bin/ansible
  python version = 2.7.16 (default, Apr 12 2019, 15:32:40) [GCC 4.2.1 Compatible Apple LLVM 10.0.1 (clang-1001.0.46.3)]
```

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
```paste below
ANSIBLE_NOCOWS(/etc/ansible/ansible.cfg) = True
ANSIBLE_PIPELINING(/etc/ansible/ansible.cfg) = True
ANSIBLE_SSH_CONTROL_PATH(/etc/ansible/ansible.cfg) = /tmp/ansible-ssh-%%h-%%p-%%r
DEFAULT_FORKS(/etc/ansible/ansible.cfg) = 20
DEFAULT_HOST_LIST(/etc/ansible/ansible.cfg) = [u'/etc/ansible/hosts']
DEFAULT_ROLES_PATH(/etc/ansible/ansible.cfg) = [u'/Users/jgeerling/Dropbox/VMs/roles']
DEFAULT_STDOUT_CALLBACK(/etc/ansible/ansible.cfg) = yaml
RETRY_FILES_ENABLED(/etc/ansible/ansible.cfg) = False
```

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->
macOS and Ubuntu

##### STEPS TO REPRODUCE

Use the `k8s_template` module inside the k8s collection:

```yaml
    - name: Test k8s_template module.
      k8s_template:
        api_version: v1
        kind: Namespace
        name: k8s-template-test
        state: present
        kubeconfig: "{{ k8s_kubeconfig }}"
```

##### EXPECTED RESULTS

There should be no failure.

##### ACTUAL RESULTS

```
    TASK [Test k8s_template module.] ***********************************************
    An exception occurred during task execution. To see the full traceback, use -vvv. The error was: ImportError: No module named json
    fatal: [localhost]: FAILED! => {"changed": false, "module_stderr": "Traceback (most recent call last):\n  File \"/Users/jgeerling/.ansible/tmp/ansible-tmp-1567187668.84-195246260630376/AnsiballZ_k8s_template.py\", line 102, in <module>\n    _ansiballz_main()\n  File \"/Users/jgeerling/.ansible/tmp/ansible-tmp-1567187668.84-195246260630376/AnsiballZ_k8s_template.py\", line 94, in _ansiballz_main\n    invoke_module(zipped_mod, temp_path, ANSIBALLZ_PARAMS)\n  File \"/Users/jgeerling/.ansible/tmp/ansible-tmp-1567187668.84-195246260630376/AnsiballZ_k8s_template.py\", line 40, in invoke_module\n    runpy.run_module(mod_name='ansible_collections.geerlingguy.k8s.plugins.modules.k8s_template', init_globals=None, run_name='__main__', alter_sys=False)\n  File \"/usr/local/Cellar/python@2/2.7.16/Frameworks/Python.framework/Versions/2.7/lib/python2.7/runpy.py\", line 192, in run_module\n    fname, loader, pkg_name)\n  File \"/usr/local/Cellar/python@2/2.7.16/Frameworks/Python.framework/Versions/2.7/lib/python2.7/runpy.py\", line 72, in _run_code\n    exec code in run_globals\n  File \"/var/folders/mt/rp7cb3s95qzfkrh1dk_8ckfc0000gn/T/ansible_k8s_template_payload_Ea45Kc/ansible_k8s_template_payload.zip/ansible_collections/geerlingguy/k8s/plugins/modules/k8s_template.py\", line 275, in <module>\n  File \"/var/folders/mt/rp7cb3s95qzfkrh1dk_8ckfc0000gn/T/ansible_k8s_template_payload_Ea45Kc/ansible_k8s_template_payload.zip/ansible_collections/geerlingguy/k8s/plugins/module_utils/k8s.py\", line 34, in <module>\n  File \"/Users/jgeerling/Downloads/ansible/lib/ansible/parsing/dataloader.py\", line 21, in <module>\n    from ansible.parsing.utils.yaml import from_yaml\n  File \"/Users/jgeerling/Downloads/ansible/lib/ansible/parsing/utils/yaml.py\", line 19, in <module>\n    from ansible.parsing.ajson import AnsibleJSONDecoder\n  File \"/Users/jgeerling/Downloads/ansible/lib/ansible/parsing/ajson.py\", line 11, in <module>\n    from ansible.module_utils.common.json import AnsibleJSONEncoder\nImportError: No module named json\n", "module_stdout": "", "msg": "MODULE FAILURE\nSee stdout/stderr for the exact error", "rc": 1}
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `0e1ec04efb10590a99bf7d6f30b2af6731a8239e` and the full history behind it is present.
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
