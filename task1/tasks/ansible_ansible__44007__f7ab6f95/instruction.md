# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Handlers are shown with wrong task name

<!---
Verify first that your issue/request is not already reported on GitHub.
THIS FORM WILL BE READ BY A MACHINE, COMPLETE ALL SECTIONS AS DESCRIBED.
Also test if the latest release, and devel branch are affected too.
ALWAYS add information AFTER (OUTSIDE) these html comments.
Otherwise it may end up being automatically closed by our bot. -->

##### SUMMARY
<!--- Explain the problem briefly -->
When handlers are run, they are displayed using a name from a previous task.

##### ISSUE TYPE
 - Bug Report

##### COMPONENT NAME
<!--- Insert, BELOW THIS COMMENT, the name of the module, plugin, task or feature.
Do not include extra details here, e.g. "vyos_command" not "the network module vyos_command" or the full path-->


##### ANSIBLE VERSION
<!--- Paste, BELOW THIS COMMENT, verbatim output from "ansible --version" between quotes below -->


##### CONFIGURATION
<!--- If using Ansible 2.4 or above, paste, BELOW THIS COMMENT, the results of "ansible-config dump --only-changed"
Otherwise, mention any settings you have changed/added/removed in ansible.cfg
(or using the ANSIBLE_* environment variables).-->

##### OS / ENVIRONMENT
<!--- Mention, BELOW THIS COMMENT, the OS you are running Ansible from, and the OS you are
managing, or say "N/A" for anything that is not platform-specific.
Also mention the specific version of what you are trying to control,
e.g. if this is a network bug the version of firmware on the network device.-->
Arch linux

##### STEPS TO REPRODUCE
<!--- For bugs, show exactly how to reproduce the problem, using a minimal test-case.
For new features, show how the feature would be used. -->

<!--- Paste example playbooks or commands between quotes below -->
```yaml
- hosts: localhost      
  tasks:                
    - name: AAA       
      debug:            
      changed_when: yes 
      notify: qqq       
    - name: BBB        
      debug:            
  handlers:             
    - name: CCC         
      debug:            
      listen: qqq       
```

<!--- You can also paste gist.github.com links for larger files -->

##### EXPECTED RESULTS
<!--- What did you expect to happen when running the steps above? -->
I would expect the handler to be shown with its name:

```
PLAY [localhost] *************************************************************************************************************************************************************************************************

TASK [AAA ] ****************************************************************************************************************************************************************************************************
changed: [localhost] => {
    "msg": "Hello world!"
}

TASK [BBB ] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Hello world!"
}

RUNNING HANDLER [CCC] ********************************************************************************************************************************************************************************************

TASK [CCC ] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Hello world!"
}

PLAY RECAP *******************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0
```

##### ACTUAL RESULTS
<!--- What actually happened? If possible run with extra verbosity (-vvvv) -->

<!--- Paste verbatim command output between quotes below -->
```
PLAY [localhost] *************************************************************************************************************************************************************************************************

TASK [AAA ] ****************************************************************************************************************************************************************************************************
changed: [localhost] => {
    "msg": "Hello world!"
}

TASK [BBB ] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Hello world!"
}

RUNNING HANDLER [CCC] ********************************************************************************************************************************************************************************************

TASK [BBB ] *****************************************************************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "Hello world!"
}

PLAY RECAP *******************************************************************************************************************************************************************************************************
localhost                  : ok=3    changed=1    unreachable=0    failed=0
```




cc @bcoca @agaffney
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `7f41f0168a7219e825711ffba853478187c26ab6` and the full history behind it is present.
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
