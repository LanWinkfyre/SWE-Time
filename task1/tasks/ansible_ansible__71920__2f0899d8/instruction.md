# Locate the commit that introduced this regression

A regression was reported against `ansible/ansible`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
ansible 2.10 fails with: An unhandled exception occurred while templating ... Error was a <class 'RecursionError'>, original message: maximum recursion depth exceeded in comparison

<!--- Verify first that your issue is not already reported on GitHub -->
<!--- Also test if the latest release and devel branch are affected too -->
<!--- Complete *all* sections as described, this form is processed automatically -->

##### SUMMARY
<!--- Explain the problem briefly below -->
I have a role that is working with ansible 2.9. When being run under ansible 2.10 (no any other change done otherwise)
it fails.

##### ISSUE TYPE
- Bug Report

##### COMPONENT NAME
<!--- Write the short name of the module, plugin, task or feature below, use your best guess if unsure -->


##### ANSIBLE VERSION
<!--- Paste verbatim output from "ansible --version" between quotes -->
```paste below
ansible 2.10.1
  config file = /srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg
  configured module search path = ['/home/spider/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /srv/app/prod/ansible/core/ansible-2.10/lib64/python3.6/site-packages/ansible
  executable location = /srv/app/prod/ansible/core/ansible-2.10/bin/ansible
  python version = 3.6.3 (default, Apr 10 2019, 14:37:36) [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)]

```

##### CONFIGURATION
<!--- Paste verbatim output from "ansible-config dump --only-changed" between quotes -->
```paste below
ANSIBLE_PIPELINING(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = True
ANSIBLE_SSH_ARGS(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = -4 -C -o ControlMaster=auto -o ControlPersist=3600s -o GSSAPIAuthentication=no -o PreferredAuthentica
ANSIBLE_SSH_CONTROL_PATH(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = /srv/tmp/prod/ansible/core/ansible-ssh-%%h-%%p-%%r
ANSIBLE_SSH_RETRIES(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = 3
CACHE_PLUGIN(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = jsonfile
CACHE_PLUGIN_CONNECTION(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = temp/cache/
CACHE_PLUGIN_PREFIX(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = json
CACHE_PLUGIN_TIMEOUT(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = 3600
DEFAULT_BECOME(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = True
DEFAULT_BECOME_ASK_PASS(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = False
DEFAULT_BECOME_METHOD(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = sudo
DEFAULT_BECOME_USER(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = root
DEFAULT_CALLBACK_WHITELIST(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = ['timer', 'log_plays']
DEFAULT_FORKS(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = 50
DEFAULT_GATHERING(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = smart
DEFAULT_HOST_LIST(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = ['/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/inventory']
DEFAULT_LOG_PATH(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = /srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/log/ansible.log
DEFAULT_MANAGED_STR(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = Ansible managed: {file}
DEFAULT_PRIVATE_KEY_FILE(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = /home/spider/.ssh/id_rsa
DEFAULT_REMOTE_USER(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = spider
DEFAULT_STRATEGY(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = free
DEFAULT_TIMEOUT(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = 10
DIFF_ALWAYS(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = True
HOST_KEY_CHECKING(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = False
RETRY_FILES_ENABLED(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = True
RETRY_FILES_SAVE_PATH(/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/ansible.cfg) = /srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/retry

```

##### OS / ENVIRONMENT
<!--- Provide all relevant information below, e.g. target OS versions, network device firmware, etc. -->
RHEL7

##### STEPS TO REPRODUCE
<!--- Describe exactly how to reproduce the problem, using a minimal test-case -->
I use task with a lot of variables and some filters to set final facts.

<!--- Paste example playbooks or commands between quotes below -->
```yaml
   - name: Add EPA records
     vars:
       epa:
         env:           "{{ item.epa.split('_')[0] }}"
         project:       "{{ item.epa.split('_')[1] }}"
         application:   "{{ item.epa.split('_')[2] }}"
         params:        { 'lv_resizefs': '{{ item.lv_resizefs | default(true) }}', 'fs_resizefs': '{{ item.fs_resizefs | default(true) }}' }
       epa_app:
         lv:            'srv_app_{{ epa.env }}_{{ epa.project }}_{{ epa.application }}'
         path:          '/srv/app/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}'
         size:          '{{ item.app_size | default(item.size) | default("1G") }}'
         fstype:        '{{ item.app_fstype | default(item.fstype) | default("ext4") }}'
         owner:         '{{ item.app_owner | default(item.owner) }}'
         group:         '{{ item.app_group | default(item.group) | default(item.app_owner) | default(item.owner) }}'
         mode:          '{{ item.app_mode | default(item.mode) | default("2770") }}'
         env_owner:     '{{ item.app_env_owner | default(item.env_owner) | default(omit) }}'
         env_group:     '{{ item.app_env_group | default(item.env_group) | default(omit) }}'
         env_mode:      "{{ item.app_env_mode | default(item.env_mode) | default('0755') }}"
         project_owner: '{{ item.app_project_owner | default(item.project_owner) | default(omit) }}'
         project_group: '{{ item.app_project_group | default(item.project_group) | default(omit) }}'
         project_mode:  "{{ item.app_project_mode | default(item.project_mode) | default('0755') }}"
       epa_bin:
         lv:            'srv_bin_{{ epa.env }}_{{ epa.project }}_{{ epa.application }}'
         path:          '/srv/bin/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}'
         size:          '{{ item.bin_size | default(item.size) | default("1G") }}'
         fstype:        '{{ item.bin_fstype | default(item.fstype) | default("ext4") }}'
         owner:         '{{ item.bin_owner | default(item.owner) }}'
         group:         '{{ item.bin_group | default(item.group) | default(item.bin_owner) | default(item.owner) }}'
         mode:          '{{ item.bin_mode | default(item.mode) | default("2770") }}'
         env_owner:     '{{ item.bin_env_owner | default(item.env_owner) | default(omit) }}'
         env_group:     '{{ item.bin_env_group | default(item.env_group) | default(omit) }}'
         env_mode:      "{{ item.bin_env_mode | default(item.env_mode) | default('0755') }}"
         project_owner: '{{ item.bin_project_owner | default(item.project_owner) | default(omit) }}'
         project_group: '{{ item.bin_project_group | default(item.project_group) | default(omit) }}'
         project_mode:  "{{ item.bin_project_mode | default(item.project_mode) | default('0755') }}"
       epa_log:
         lv:            'srv_log_{{ epa.env }}_{{ epa.project }}_{{ epa.application }}'
         path:          '/srv/log/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}'
         size:          '{{ item.log_size | default(item.size) | default("1G") }}'
         fstype:        '{{ item.log_fstype | default(item.fstype) | default("ext4") }}'
         owner:         '{{ item.log_owner | default(item.owner) }}'
         group:         '{{ item.log_group | default(item.group) | default(item.log_owner) | default(item.owner) }}'
         mode:          '{{ item.log_mode | default(item.mode) | default("2770") }}'
         env_owner:     '{{ item.log_env_owner | default(item.env_owner) | default(omit) }}'
         env_group:     '{{ item.log_env_group | default(item.env_group) | default(omit) }}'
         env_mode:      "{{ item.log_env_mode | default(item.env_mode) | default('0755') }}"
         project_owner: '{{ item.log_project_owner | default(item.project_owner) | default(omit) }}'
         project_group: '{{ item.log_project_group | default(item.project_group) | default(omit) }}'
         project_mode:  "{{ item.log_project_mode | default(item.project_mode) | default('0755') }}"
       epa_tmp:
         lv:            'srv_tmp_{{ epa.env }}_{{ epa.project }}_{{ epa.application }}'
         path:          '/srv/tmp/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}'
         size:          '{{ item.tmp_size | default(item.size) | default("1G") }}'
         fstype:        '{{ item.tmp_fstype | default(item.fstype) | default("ext4") }}'
         owner:         '{{ item.tmp_owner | default(item.owner) }}'
         group:         '{{ item.tmp_group | default(item.group) | default(item.tmp_owner) | default(item.owner) }}'
         mode:          '{{ item.tmp_mode | default(item.mode) | default("2770") }}'
         env_owner:     '{{ item.tmp_env_owner | default(item.env_owner) | default(omit) }}'
         env_group:     '{{ item.tmp_env_group | default(item.env_group) | default(omit) }}'
         env_mode:      "{{ item.tmp_env_mode | default(item.env_mode) | default('0755') }}"
         project_owner: '{{ item.tmp_project_owner | default(item.project_owner) | default(omit) }}'
         project_group: '{{ item.tmp_project_group | default(item.project_group) | default(omit) }}'
         project_mode:  "{{ item.tmp_project_mode | default(item.project_mode) | default('0755') }}"
       epa_data:
         lv:            'srv_data_{{ epa.env }}_{{ epa.project }}_{{ epa.application }}_local_{{ item.data_name | default(epa.application) }}'
         path:          '/srv/data/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}/local/{{ item.data_name | default(epa.application) }}'
         size:          '{{ item.data_size | default(item.size) | default("1G") }}'
         fstype:        '{{ item.data_fstype | default(item.fstype) | default("ext4") }}'
         owner:         '{{ item.data_owner | default(item.owner) }}'
         group:         '{{ item.data_group | default(item.group) | default(item.data_owner) | default(item.owner) }}'
         mode:          '{{ item.data_mode | default(item.mode) | default("2770") }}'
         env_owner:     '{{ item.data_env_owner | default(item.env_owner) | default(omit) }}'
         env_group:     '{{ item.data_env_group | default(item.env_group) | default(omit) }}'
         env_mode:      "{{ item.data_env_mode | default(item.env_mode) | default('0755') }}"
         project_owner: '{{ item.data_project_owner | default(item.project_owner) | default(omit) }}'
         project_group: '{{ item.data_project_group | default(item.project_group) | default(omit) }}'
         project_mode:  "{{ item.data_project_mode | default(item.project_mode) | default('0755') }}"
       epa_sasbin:
         lv:            'srv_sasbin_{{ epa.env }}_{{ epa.project }}_{{ epa.application }}'
         path:          '/srv/sasbin/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}'
         size:          '{{ item.sasbin_size | default(false) }}'
         fstype:        '{{ item.sasbin_fstype | default(item.fstype) | default("ext4") }}'
         owner:         '{{ item.sasbin_owner | default(item.owner) }}'
         group:         '{{ item.sasbin_group | default(item.group) | default(item.sasbin_owner) | default(item.owner) }}'
         mode:          '{{ item.sasbin_mode | default(item.mode) | default("2770") }}'
         env_owner:     '{{ item.sasbin_env_owner | default(item.env_owner) | default(omit) }}'
         env_group:     '{{ item.sasbin_env_group | default(item.env_group) | default(omit) }}'
         env_mode:      "{{ item.sasbin_env_mode | default(item.env_mode) | default('0755') }}"
         project_owner: '{{ item.sasbin_project_owner | default(item.project_owner) | default(omit) }}'
         project_group: '{{ item.sasbin_project_group | default(item.project_group) | default(omit) }}'
         project_mode:  "{{ item.sasbin_project_mode | default(item.project_mode) | default('0755') }}"
       epa_app_vol:     '{{ [ item | combine(epa_app, recursive = True)    | combine(epa.params, recursive = True) ] }}'
       epa_bin_vol:     '{{ [ item | combine(epa_bin, recursive = True)    | combine(epa.params, recursive = True) ] }}'
       epa_log_vol:     '{{ [ item | combine(epa_log, recursive = True)    | combine(epa.params, recursive = True) ] }}'
       epa_tmp_vol:     '{{ [ item | combine(epa_tmp, recursive = True)    | combine(epa.params, recursive = True) ] }}'
       epa_data_vol:    '{{ [ item | combine(epa_data, recursive = True)   | combine(epa.params, recursive = True) ] }}'
       epa_sasbin_vol:  '{{ [ item | combine(epa_sasbin, recursive = True) | combine(epa.params, recursive = True) ] }}'
       epa_volumes:     "{{ ( epa_app_vol + epa_bin_vol + epa_log_vol + epa_tmp_vol + epa_data_vol + epa_sasbin_vol ) | rejectattr('size', 'equalto', '0') | rejectattr('size', 'equalto', False) | list }}"
       epa_manage_files_fs:
         - { 'path': '/srv',        'state': 'directory' }
         - { 'path': '/srv/app',    'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/bin',    'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/log',    'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/tmp',    'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/data',   'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/sasbin', 'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/app/{{ epa.env }}',    'state': 'directory', 'owner': '{{ epa_app.env_owner | default(omit) }}',    'group': '{{ epa_app.env_group | default(omit) }}',    'mode': '{{ epa_app.env_mode | default(omit) }}' }
         - { 'path': '/srv/bin/{{ epa.env }}',    'state': 'directory', 'owner': '{{ epa_bin.env_owner | default(omit) }}',    'group': '{{ epa_bin.env_group | default(omit) }}',    'mode': '{{ epa_bin.env_mode | default(omit) }}' }
         - { 'path': '/srv/log/{{ epa.env }}',    'state': 'directory', 'owner': '{{ epa_log.env_owner | default(omit) }}',    'group': '{{ epa_log.env_group | default(omit) }}',    'mode': '{{ epa_log.env_mode | default(omit) }}' }
         - { 'path': '/srv/tmp/{{ epa.env }}',    'state': 'directory', 'owner': '{{ epa_tmp.env_owner | default(omit) }}',    'group': '{{ epa_tmp.env_group | default(omit) }}',    'mode': '{{ epa_tmp.env_mode | default(omit) }}' }
         - { 'path': '/srv/data/{{ epa.env }}',   'state': 'directory', 'owner': '{{ epa_data.env_owner | default(omit) }}',   'group': '{{ epa_data.env_group | default(omit) }}',   'mode': '{{ epa_data.env_mode | default(omit) }}' }
         - { 'path': '/srv/sasbin/{{ epa.env }}', 'state': 'directory', 'owner': '{{ epa_sasbin.env_owner | default(omit) }}', 'group': '{{ epa_sasbin.env_group | default(omit) }}', 'mode': '{{ epa_sasbin.env_mode | default(omit) }}' }
         - { 'path': '/srv/app/{{ epa.env }}/{{ epa.project }}',    'state': 'directory', 'owner': '{{ epa_app.project_owner | default(omit) }}',    'group': '{{ epa_app.project_group | default(omit) }}',    'mode': '{{ epa_app.project_mode | default(omit) }}' }
         - { 'path': '/srv/bin/{{ epa.env }}/{{ epa.project }}',    'state': 'directory', 'owner': '{{ epa_bin.project_owner | default(omit) }}',    'group': '{{ epa_bin.project_group | default(omit) }}',    'mode': '{{ epa_bin.project_mode | default(omit) }}' }
         - { 'path': '/srv/log/{{ epa.env }}/{{ epa.project }}',    'state': 'directory', 'owner': '{{ epa_log.project_owner | default(omit) }}',    'group': '{{ epa_log.project_group | default(omit) }}',    'mode': '{{ epa_log.project_mode | default(omit) }}' }
         - { 'path': '/srv/tmp/{{ epa.env }}/{{ epa.project }}',    'state': 'directory', 'owner': '{{ epa_tmp.project_owner | default(omit) }}',    'group': '{{ epa_tmp.project_group | default(omit) }}',    'mode': '{{ epa_tmp.project_mode | default(omit) }}' }
         - { 'path': '/srv/data/{{ epa.env }}/{{ epa.project }}',   'state': 'directory', 'owner': '{{ epa_data.project_owner | default(omit) }}',   'group': '{{ epa_data.project_group | default(omit) }}',   'mode': '{{ epa_data.project_mode | default(omit) }}' }
         - { 'path': '/srv/sasbin/{{ epa.env }}/{{ epa.project }}', 'state': 'directory', 'owner': '{{ epa_sasbin.project_owner | default(omit) }}', 'group': '{{ epa_sasbin.project_group | default(omit) }}', 'mode': '{{ epa_sasbin.project_mode | default(omit) }}' }
         - { 'path': '/srv/data/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}', 'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/data/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}/local', 'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
         - { 'path': '/srv/data/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}/remote', 'state': 'directory', 'owner': 'root', 'group': 'root', 'mode': '0755' }
     set_fact:
       main_role_csas_epa_volumes:         "{{ main_role_csas_epa_volumes + epa_volumes }}"
       main_role_csas_epa_manage_files_fs: "{{ main_role_csas_epa_manage_files_fs + epa_manage_files_fs }}"
     loop: '{{ main_role_csas_epa_epas }}'

   - name: Remove duplicate records from managed files
     set_fact:
       main_role_csas_epa_manage_files_fs: "{{ main_role_csas_epa_manage_files_fs | unique }}"
  when: main_role_csas_epa_epas is defined and main_role_csas_epa_epas | length > 0
  tags:
    - role_csas_epa_volume
    - role_csas_epa_volumes
    - role_csas_epa_manage_file_fs
    - role_csas_epa_manage_files_fs
```

<!--- HINT: You can paste gist.github.com links for larger files -->

##### EXPECTED RESULTS
<!--- Describe what you expected to happen when running the steps above -->
this is a result with ansible 2.9:

TASK [csas_epa : Add EPA records] ***********************************************************************************************************************************************************
ok: [tpinsas03.vs.csin.cz] => (item={'epa': 'prod_cman_test', 'owner': 'pepa', 'tmp_size': '0', 'log_size': '0', 'data_size': '0', 'bin_size': '0', 'app_size': '1g', 'sasbin_size': '1g'})
ok: [tpinsas03.vs.csin.cz] => (item={'epa': 'prod_cman_pica', 'owner': 'pepa', 'tmp_size': '0', 'log_size': '1g', 'data_size': '1g', 'bin_size': False, 'app_size': '1g', 'apache': True})
ok: [tpinsas03.vs.csin.cz] => (item={'epa': 'tst_dion_kurva', 'owner': 'karel', 'group': 'pepa', 'tmp_size': '5g', 'tmp_mode': '1777', 'env_owner': 'karel', 'tmp_owner': 'pepa', 'tmp_env_owner': 'pepa'})
ok: [tpinsas03.vs.csin.cz] => (item={'epa': 'prod_apache_blah', 'owner': 'pepa', 'tmp_size': '0', 'log_size': '1g', 'data_size': '1g', 'bin_size': False, 'app_size': '1g', 'apache': True})
ok: [tpinsas03.vs.csin.cz] => (item={'epa': 'prod_apache_bar', 'owner': 'karel', 'tmp_size': '1g', 'log_size': '1g', 'data_size': '1g', 'bin_size': False, 'app_size': '1g', 'apache': True, 'data_name': 'foobar'})
 [started TASK: csas_epa : Remove duplicate records from managed files on tpinsas03.vs.csin.cz]

TASK [csas_epa : Remove duplicate records from managed files] *******************************************************************************************************************************
ok: [tpinsas03.vs.csin.cz]
 [started TASK: csas_epa : Add Apache into EPA(s) on tpinsas03.vs.csin.cz]


##### ACTUAL RESULTS
<!--- Describe what actually happened. If possible run with extra verbosity (-vvvv) -->
Ansible 2.10 fails with:

"An unhandled exception occurred while templating ... Error was a <class 'RecursionError'>, original message: maximum recursion depth exceeded in comparison"

<!--- Paste verbatim command output between quotes -->
```paste below

TASK [csas_epa : Add EPA records] ***********************************************************************************************************************************************************
fatal: [tpinsas03.vs.csin.cz]: FAILED! => {"msg": "An unhandled exception occurred while templating '[AnsibleMapping([('path', '/srv'), ('state', 'directory')]), AnsibleMapping([('path', '/srv/app'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/bin'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/log'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/tmp'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/data'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/sasbin'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/app/{{ epa.env }}'), ('state', 'directory'), ('owner', '{{ epa_app.env_owner | default(omit) }}'), ('group', '{{ epa_app.env_group | default(omit) }}'), ('mode', '{{ epa_app.env_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/bin/{{ epa.env }}'), ('state', 'directory'), ('owner', '{{ epa_bin.env_owner | default(omit) }}'), ('group', '{{ epa_bin.env_group | default(omit) }}'), ('mode', '{{ epa_bin.env_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/log/{{ epa.env }}'), ('state', 'directory'), ('owner', '{{ epa_log.env_owner | default(omit) }}'), ('group', '{{ epa_log.env_group | default(omit) }}'), ('mode', '{{ epa_log.env_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/tmp/{{ epa.env }}'), ('state', 'directory'), ('owner', '{{ epa_tmp.env_owner | default(omit) }}'), ('group', '{{ epa_tmp.env_group | default(omit) }}'), ('mode', '{{ epa_tmp.env_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/data/{{ epa.env }}'), ('state', 'directory'), ('owner', '{{ epa_data.env_owner | default(omit) }}'), ('group', '{{ epa_data.env_group | default(omit) }}'), ('mode', '{{ epa_data.env_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/sasbin/{{ epa.env }}'), ('state', 'directory'), ('owner', '{{ epa_sasbin.env_owner | default(omit) }}'), ('group', '{{ epa_sasbin.env_group | default(omit) }}'), ('mode', '{{ epa_sasbin.env_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/app/{{ epa.env }}/{{ epa.project }}'), ('state', 'directory'), ('owner', '{{ epa_app.project_owner | default(omit) }}'), ('group', '{{ epa_app.project_group | default(omit) }}'), ('mode', '{{ epa_app.project_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/bin/{{ epa.env }}/{{ epa.project }}'), ('state', 'directory'), ('owner', '{{ epa_bin.project_owner | default(omit) }}'), ('group', '{{ epa_bin.project_group | default(omit) }}'), ('mode', '{{ epa_bin.project_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/log/{{ epa.env }}/{{ epa.project }}'), ('state', 'directory'), ('owner', '{{ epa_log.project_owner | default(omit) }}'), ('group', '{{ epa_log.project_group | default(omit) }}'), ('mode', '{{ epa_log.project_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/tmp/{{ epa.env }}/{{ epa.project }}'), ('state', 'directory'), ('owner', '{{ epa_tmp.project_owner | default(omit) }}'), ('group', '{{ epa_tmp.project_group | default(omit) }}'), ('mode', '{{ epa_tmp.project_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/data/{{ epa.env }}/{{ epa.project }}'), ('state', 'directory'), ('owner', '{{ epa_data.project_owner | default(omit) }}'), ('group', '{{ epa_data.project_group | default(omit) }}'), ('mode', '{{ epa_data.project_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/sasbin/{{ epa.env }}/{{ epa.project }}'), ('state', 'directory'), ('owner', '{{ epa_sasbin.project_owner | default(omit) }}'), ('group', '{{ epa_sasbin.project_group | default(omit) }}'), ('mode', '{{ epa_sasbin.project_mode | default(omit) }}')]), AnsibleMapping([('path', '/srv/data/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/data/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}/local'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')]), AnsibleMapping([('path', '/srv/data/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}/remote'), ('state', 'directory'), ('owner', 'root'), ('group', 'root'), ('mode', '0755')])]'. Error was a <class 'ansible.errors.AnsibleError'>, original message: An unhandled exception occurred while templating 'AnsibleMapping([('lv', 'srv_tmp_{{ epa.env }}_{{ epa.project }}_{{ epa.application }}'), ('path', '/srv/tmp/{{ epa.env }}/{{ epa.project }}/{{ epa.application }}'), ('size', '{{ item.tmp_size | default(item.size) | default(\"1G\") }}'), ('fstype', '{{ item.tmp_fstype | default(item.fstype) | default(\"ext4\") }}'), ('owner', '{{ item.tmp_owner | default(item.owner) }}'), ('group', '{{ item.tmp_group | default(item.group) | default(item.tmp_owner) | default(item.owner) }}'), ('mode', '{{ item.tmp_mode | default(item.mode) | default(\"2770\") }}'), ('env_owner', '{{ item.tmp_env_owner | default(item.env_owner) | default(omit) }}'), ('env_group', '{{ item.tmp_env_group | default(item.env_group) | default(omit) }}'), ('env_mode', \"{{ item.tmp_env_mode | default(item.env_mode) | default('0755') }}\"), ('project_owner', '{{ item.tmp_project_owner | default(item.project_owner) | default(omit) }}'), ('project_group', '{{ item.tmp_project_group | default(item.project_group) | default(omit) }}'), ('project_mode', \"{{ item.tmp_project_mode | default(item.project_mode) | default('0755') }}\")])'. Error was a <class 'RecursionError'>, original message: maximum recursion depth exceeded in comparison"}
        to retry, use: --limit @/srv/data/prod/ansible/core/remote/cm/csas/linux-cm-dev/retry/csas_cm_dynamic.retry

PLAY RECAP **********************************************************************************************************************************************************************************
tpinsas03.vs.csin.cz       : ok=10   changed=0    unreachable=0    failed=1    skipped=2    rescued=0    ignored=0

```


Thank you for providing the easy reproducers. I was not able to get `test.yml` to fail when using `devel`. I was able to get `test_full.yml` to fail.



Anecdotally I did observe it took longer to template as I moved forward in the commit history. I will have to measure and test more to see if I can see at what point it started taking longer to template.
```

## What you have

- `/testbed/repo` is a git clone of `ansible/ansible` truncated just after the regression was
  reported.  `HEAD` is `70e25dc15828614a1e937567c8023bf0f33b8143` and the full history behind it is present.
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
