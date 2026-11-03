# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`ansible-galaxy collection install` explodes for some collections on `devel`

#### SUMMARY
<!--- Explain the problem briefly below -->
Installing `amazon.aws` collection fails on ansible/ansible@devel, supposedly because of the embedded symlinks:
```console
ERROR! Unexpected Exception, this is probably a bug: "filename 'tests/unit/mod
ules/placebo_recordings/aws_direct_connect_link_aggregation_group/nonexistent_
lag_status' not found"
```

##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME
<!--- Write the short name of the module, plugin, task or feature below, use your best guess if unsure -->
ansible-galaxy CLI

##### ANSIBLE VERSION
<!--- Paste verbatim output from "ansible --version" between quotes -->
devel

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
N/A

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->
N/A

##### STEPS TO REPRODUCE
<!--- Describe exactly how to reproduce the problem, using a minimal test-case -->
Running the install should be enough:
<!--- Paste example playbooks or commands between quotes below -->
```console
$ ANSIBLE_DEBUG=1 ansible-galaxy -vvvv collection install amazon.aws
```

##### EXPECTED RESULTS
<!--- Describe what you expected to happen when running the steps above -->
The collection install should succeed.

##### ACTUAL RESULTS
<!--- Describe what actually happened. If possible run with extra verbosity (-vvvv) -->

<!--- Paste verbatim command output between quotes -->
```python-traceback
Exception, this is probably a bug: "filename 'tests/unit/modules/placebo_recordings/aws_direct_connect_link_aggregation_group/nonexistent_lag_status' not found"
the full traceback was:
Traceback (most recent call last):
  File "/home/bcoca/work/ansible/bin/ansible-galaxy", line 123, in <module>
    exit_code = cli.run()
  File "/home/bcoca/work/ansible/lib/ansible/cli/galaxy.py", line 490, in run
    context.CLIARGS['func']()
  File "/home/bcoca/work/ansible/lib/ansible/cli/galaxy.py", line 1057, in execute_install
    self._execute_install_collection(collection_requirements, collection_path)
  File "/home/bcoca/work/ansible/lib/ansible/cli/galaxy.py", line 1079, in _execute_install_collection
    no_deps, force, force_with_deps, allow_pre_release=allow_pre_release)
  File "/home/bcoca/work/ansible/lib/ansible/galaxy/collection.py", line 675, in install_collections
    collection.install(output_path, b_temp_path)
  File "/home/bcoca/work/ansible/lib/ansible/galaxy/collection.py", line 250, in install
    self.install_artifact(b_collection_path, b_temp_path)
  File "/home/bcoca/work/ansible/lib/ansible/galaxy/collection.py", line 275, in install_artifact
    _extract_tar_dir(collection_tar, file_name, b_collection_path)
  File "/home/bcoca/work/ansible/lib/ansible/galaxy/collection.py", line 1387, in _extract_tar_dir
    tar_member = tar.getmember(to_native(dirname, errors='surrogate_or_strict'))
  File "/usr/lib/python3.7/tarfile.py", line 1752, in getmember
    raise KeyError("filename %r not found" % name)
KeyError: "filename 'tests/unit/modules/placebo_recordings/aws_direct_connect_link_aggregation_group/nonexistent_lag_status' not found"
```
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `ebb22655e42f944cfa898488a7cfd3003297ecfe` and the full history behind it is present.
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
