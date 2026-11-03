# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
test_exec_basic fails in mkosi after updating to systemd v247

**systemd version the issue has been seen with**
 > master branch

**Used distribution**
 > Arch

**Linux kernel version used** (`uname -a`)
 > 5.9.11

**CPU architecture issue was seen on**
 > x86_64

**Expected behaviour you didn't see**
 > Tests pass

**Unexpected behaviour you saw**
 > test_exec_basic fails

**Steps to reproduce the problem**
 > sudo mkosi --default .mkosi/mkosi.fedora (or any distro of your choice)

 

```
292/417 test-execute                              FAIL           0.12s (killed by signal 6 SIGABRT)

--- command ---
18:07:13 SYSTEMD_LANGUAGE_FALLBACK_MAP='/root/src/src/locale/language-fallback-map' PATH='/root/build:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin' SYSTEMD_KBD_MODEL_MAP='/root/src/src/locale/kbd-model-map' /root/build/test-execute
--- Listing only the last 100 lines from a long log. ---
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-environment-no-substitute.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-systemcallfilter-failing2.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-passenvironment-repeated.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-standardinput-data.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-systemcallfilter-with-errno-number.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-dynamicuser-fixeduser-games.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-capabilityboundingset-merge.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-umask-default.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-privatedevices-yes-capability-mknod.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-readwritepaths-mount-propagation.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-runtimedirectory-owner-nfsnobody.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-protectkernellogs-no-capabilities.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-privatedevices-no.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-privatedevices-no-capability-mknod.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-protectkernelmodules-yes-capabilities.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-dynamicuser-fixeduser-adm.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-supplementarygroups-multiple-groups-default-group-user.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-systemcallfilter-not-failing.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-protectkernelmodules-yes-mount-propagation.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-supplementarygroups-multiple-groups-withgid.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-privatedevices-disabled-by-prefix.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-ambientcapabilities-merge.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-readonlypaths-mount-propagation.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-user-nfsnobody.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-personality-ppc64le.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-environment.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-systemcallfilter-not-failing2.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-supplementarygroups-single-group-user.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-protecthome-tmpfs-vs-protectsystem-strict.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-environment-empty.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-privatedevices-yes-capability-sys-rawio.service
unit_file_build_name_map: normal unit file: /root/src/test/test-execute/exec-restrictnamespaces-mnt.service
proc.mount: Failed to load configuration: No such file or directory
proc-sys.mount: Failed to load configuration: No such file or directory
proc-sys-kernel.mount: Failed to load configuration: No such file or directory
proc-sys-kernel-random.mount: Failed to load configuration: No such file or directory
sys.mount: Failed to load configuration: No such file or directory
dev.mount: Failed to load configuration: No such file or directory
var.mount: Failed to load configuration: No such file or directory
root.mount: Failed to load configuration: No such file or directory
run.mount: Failed to load configuration: No such file or directory
SELinux enabled state cached to: disabled
Successfully created private D-Bus server.
Bus bus-system: changing state UNSET → OPENING
Bus bus-system: changing state OPENING → CLOSED
Failed to connect to system bus: No such file or directory
Invoking unit coldplug() handlers…
-.slice changed dead -> active
efi.mount: Changed dead -> mounted
root-dest.mount: Changed dead -> mounted
sys-devices.mount: Changed dead -> mounted
proc-fs.mount: Changed dead -> mounted
proc-bus.mount: Changed dead -> mounted
sys-kernel.mount: Changed dead -> mounted
root-build.mount: Changed dead -> mounted
proc-acpi.mount: Changed dead -> mounted
proc-sys-net.mount: Changed dead -> mounted
run-host.mount: Changed dead -> mounted
-.mount: Changed dead -> mounted
sys-dev.mount: Changed dead -> mounted
dev-mqueue.mount: Changed dead -> mounted
init.scope changed dead -> running
run-host-os\x2drelease.mount: Changed dead -> mounted
proc-asound.mount: Changed dead -> mounted
var-tmp.mount: Changed dead -> mounted
proc-sys-kernel-random-boot_id.mount: Changed dead -> mounted
sys-class.mount: Changed dead -> mounted
tmp.mount: Changed dead -> mounted
sys-block.mount: Changed dead -> mounted
proc-scsi.mount: Changed dead -> mounted
sys-bus.mount: Changed dead -> mounted
run-host-incoming.mount: Changed dead -> mounted
proc-irq.mount: Changed dead -> mounted
Invoking unit catchup() handlers…
shutdown.target: Failed to load configuration: No such file or directory
basic.target: Failed to load configuration: No such file or directory
exec-basic.service: ConditionKernelVersion=" >= 2.0" " * " "*.*" succeeded.
exec-basic.service: ConditionKernelVersion=" >= 2.0" " <= 60 " "!= 1.4" succeeded.
exec-basic.service: ConditionKernelVersion=">=2.0" "<=60" "!=1.4" succeeded.
exec-basic.service: ConditionKernelVersion=">=3.0" succeeded.
exec-basic.service: Failed to set 'memory.limit_in_bytes' attribute on '/8f23b4c65cdebd7/exec-basic.service' to '-1': No such file or directory
exec-basic.service: Failed to set 'pids.max' attribute on '/8f23b4c65cdebd7/exec-basic.service' to 'max': No such file or directory
exec-basic.service: Passing 0 fds to service
exec-basic.service: About to execute: /usr/bin/touch /tmp/a
exec-basic.service: Forked /usr/bin/touch as 6196
exec-basic.service: Changed dead -> start
Received SIGCHLD from PID 6196 ((touch)).
Child 6196 ((touch)) died (code=exited, status=226/NAMESPACE)
exec-basic.service: Failed to read oom_kill field of memory.events cgroup attribute: No such file or directory
exec-basic.service: Child 6196 belongs to exec-basic.service.
exec-basic.service: Main process exited, code=exited, status=226/NAMESPACE
exec-basic.service: Failed with result 'exit-code'.
exec-basic.service: Service will not restart (restart setting)
exec-basic.service: Changed start -> failed
exec-basic.service: Unit entered failed state.
Spawning thread to nuke /tmp/systemd-private-b2d70b4916b64f00b671ddd76882c67d-exec-basic.service-DZkrir
Spawning thread to nuke /var/tmp/systemd-private-b2d70b4916b64f00b671ddd76882c67d-exec-basic.service-vBuyIr
test_exec_basic: exec-basic.service: exit status 226, expected 0
-------

Full log written to /root/build/meson-logs/testlog.txt
FAILED: meson-test 
/usr/bin/meson test --no-rebuild --print-errorlogs
ninja: build stopped: subcommand failed.
‣ Error: Build script returned non-zero exit code 1.
```
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `6dd16814a56d2ce96ab3c4c611a61e47f2f7b663` and the full history behind it is present.
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
