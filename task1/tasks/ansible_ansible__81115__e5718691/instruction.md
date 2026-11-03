# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
"service_facts" module cannot report whether a service is enabled or not if it is in "failed" state

### Summary

I use a playbook that handles failures and restarts a service if it is enabled on a server, and does nothing if it is disabled. To detect whether the playbook should take action on the service, it relies on the `service_facts` module.

```
- name: Get service facts:
  service_facts:
  become: yes

- name: Act on the service
  vars:
    app_service: 'foo.service'
    app_service_cache_dir: '/var/cache/foo'
    app_service_user: 'foo'
  when: 'ansible_facts.services[app_service].status == "enabled" '
  block:

    - name: Stop service
      service:
        name: "{{ app_service }}"
        state: stopped
      become: yes

    - name: Clear the cache folder
      file:
        path: "{{ app_service_cache_dir }}"
        state: absent
      become: yes
  
    - name: Recreate the cache folder
      file:
        path: "{{ app_service_cache_dir }}"
        state: directory
        owner: "{{ app_service_user }}"
        mode: "0700"
      become: yes

    - name: Start service
      service:
        name: "{{ app_service }}"
        state: started
      become: yes
```

The playbook was working fine under Ansible 2.9.27, however it has stopped working under Ansible 2.14.2 if the service enters a _failed_ state in systemd (for example, in case it crashes). Under Ansible 2.14.2, the `service_facts` module sets the `status` attribute to `failed` and, as a result, it is no longer possible to figure out from existing service facts whether the playbook should act on the service or not. As a workaround, I had to manually invoke `systemctl is-enabled foo.service` with the `command` module.





I may have code the playbook incorrectly. By reading the existing documentation about the `service_facts` module, I could not figure out the attribute that says whether a service is configured to start at boot time or not, nor the attribute that says whether the service is currently running or not. The definitions of `status` and `state` attributes don't seem clear.

### Issue Type

Bug Report

### Component Name

service_facts

### Ansible Version




### Configuration

```console
# if using a version older than ansible-core 2.12 you should omit the '-t all'
$ ansible-config dump --only-changed -t all
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can become unstable at any point.
```


### OS / Environment

CentOS Stream 9

### Steps to Reproduce

<!--- Paste example playbooks or commands between quotes below -->

This is a minimal playbook that reproduces the issue.

```yaml (paste below)
---
# service_facts.yml
- hosts: localhost
  gather_facts: no
  vars:
    test_service: 'foo.service'
  tasks:

    - name: Ensure that a failed service exists
      block:

        - name: Verify whether a failed service exists
          command:
            argv:
              - systemctl
              - 'is-failed'
              - "{{ test_service }}"

      rescue:

        - name: Install a service that fails
          copy:
            content: |
              [Unit]
              After=local-fs.target

              [Service]
              Type=simple
              ExecStart=/bin/false

              [Install]
              WantedBy=multi-user.target
            dest: "/etc/systemd/system/{{ test_service }}"
          become: yes

        - name: Reload systemd and start the test service
          systemd:
            name: "{{ test_service }}"
            state: started
            daemon_reload: yes
          become: yes
          ignore_errors: yes

        - name: Ensure that the installed failed service exists
          command:
            argv:
              - systemctl
              - 'is-failed'
              - "{{ test_service }}"

    - name: Ensure that the failed service is disabled
      systemd:
        name: "{{ test_service }}"
        enabled: no
      become: yes

    - name: Get service facts
      service_facts:
      become: yes

    - name: Store facts about the failed service that is disabled
      set_fact:
        test_service_disabled: "{{ ansible_facts.services[test_service] | dict2items }}"

    - name: Ensure that the failed service is enabled
      systemd:
        name: "{{ test_service }}"
        enabled: yes
      become: yes

    - name: Get service facts again
      service_facts:
      become: yes

    - name: Store facts about the failed service that is enabled
      set_fact:
        test_service_enabled: "{{ ansible_facts.services[test_service] | dict2items }}"

    - name: Compare service details
      vars:
        test_service_symmetric_diff: "{{ test_service_disabled | symmetric_difference(test_service_enabled) }}"
      assert:
        that:
          - '(test_service_symmetric_diff | length) > 0'
        success_msg: "service information is different: '{{ test_service_symmetric_diff | to_json }}'"
        fail_msg: "! service information is equal !!! '{{ test_service_disabled | to_json }}'"
```

This is the script used with `git bisect`.

```
#!/bin/bash
set -o pipefail
curdir="${0}"
[ -h "${curdir}" ] && curdir="`readlink -f \"${curdir}\"`"
curdir="`dirname \"${curdir}\"`"
. "${curdir}/ansible/hacking/env-setup" -q
tempfile="`mktemp`"
[ -f "${tempfile}" ] || exit 125
if ansible-playbook "${curdir}/service_facts.yml" | tee "${tempfile}"; then
    rm -f "${tempfile}"
    exit 0
elif tail --lines=10 "${tempfile}" | grep -qF '! service information is equal !!!'; then
    rm -f "${tempfile}"
    exit 1
else
    rm -fv "${tempfile}"
    exit 125
fi
```

### Expected Results

After invoking the `service_facts` module to get information about a service that has entered a _failed_ state on a managed host, it should be possible to identify whether a service is enabled or not (that is, whether a service is configured to start at boot time or not).

### Actual Results




### Code of Conduct

- [X] I agree to follow the Ansible Code of Conduct
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `da2cd157f151ad1244296df54603698075faf5d2` and the full history behind it is present.
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
