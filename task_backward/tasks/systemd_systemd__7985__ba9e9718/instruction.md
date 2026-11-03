# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[bisected] fails to boot when `systemd.log_level=debug`

### Submission type

 - Bug report

<!-- **NOTE:** Do not submit anything other than bug reports or RFEs via the issue tracker! -->

### systemd version the issue has been seen with

I was convinced this was going to point to my mount logging change.  






<!-- **NOTE:** Do not submit bug reports about anything but the two most recently released systemd versions upstream! -->
<!-- For older version please use distribution trackers (see https://github.com/systemd/systemd/blob/master/.github/CONTRIBUTING.md#filing-issues). -->

### Used distribution

Fedora 27.  Selinux is disabled.

I made sure to install the same version of systemd to the initramfs (`dracut --force`).

### In case of bug report: Expected behaviour you didn't see

boot success

### In case of bug report: Unexpected behaviour you saw

System enters emergency mode.

**EDIT**: *processes on the critical path to mount /boot are blocked.  Trying to write to the journal, but systemd hasn't started it... because it's blocked trying to write to the journal.*

It looks like we're now always losing the race to start journald, before we've filled up the journald socket buffer.  (I wonder what reasons there are to open that race. Maybe we should be more robust - have journald open its own sockets.)

```
[  OK  ] Mounted Kernel Debug File System.
[   13.295230] kauditd_printk_skb: 48 callbacks suppressed
[   13.295232] audit: type=1130 audit(1516793691.603:59): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=kmod-static-nodes comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[  OK  ] Mounted POSIX Message Queue File System.
[   ***] (7 of 8) A start job is running for Journal Service (20s / 1min 30s)[   24.063792] EXT4-fs (vda3): re-mounted. Opts: (null)
[  OK  ] Started udev Coldplug all Devices.
[   24.075129] audit: type=1130 audit(1516793702.384:60): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udev-trigger comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
         Starting udev Wait for Complete Device Initialization...
[***   ] (3 of 8) A start job is running for…ce Initialization (30s / 3min 20s)[   34.275201] audit: type=1130 audit(1516793712.584:61): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-remount-fs comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[  OK  ] Started Remount Root and Kernel File Systems.
         Starting Configure read-only root support...
         Starting Rebuild Hardware Database...
         Starting Create System Users...
[**    ] (4 of 10) A start job is running fo…ce Initialization (41s / 3min 20s)[   44.557244] audit: type=1130 audit(1516793722.867:62): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=fedora-readonly comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[  OK  ] Started Configure read-only root support.
         Starting Load/Save Random Seed...
[  OK  [[   45.083112] audit: type=1130 audit(1516793723.392:63): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-hwdb-update comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
0m] Started Rebuild Hardware Database.
[   ***] (9 of 9) A start job is running for…reate System Users (51s / 2min 1s)[   54.763187] audit: type=1130 audit(1516793733.073:64): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-random-seed comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[  OK  ] Started Load/Save Random Seed.
[  *** ] (3 of 8) A start job is running for…itialization (1min 10s / 3min 20s)[   73.890347] audit: type=1131 audit(1516793752.200:65): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=lvm2-lvmpolld comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[ TIME ] Timed out waiting for device dev-ttyS0.device.
[DEPEND] Dependency failed for Serial Getty on ttyS0.
[ TIME ] Timed out waiting for device dev-di…75\x2d96f9\x2d4f63b9a04c83.device.
[DEPEND] Dependency failed for /boot.
[DEPEND] Dependency failed for Local File Systems.
[DEPEND] Dependency failed for Mark the need to relabel after reboot.
[DEPEND] Dependency failed for File System C…c55a0-75b1-4a75-96f9-4f63b9a04c83.
[FAILED] Failed to start Journal Service.
See 'systemctl status systemd-journald.service' for details.
[DEPEND] Dependency failed for Flush Journal to Persistent Storage.
[ TIME ] Timed out waiting for device dev-di…6b\x2dae10\x2da59eb6324f28.device.
[DEPEND] Dependency failed for /dev/disk/by-…a285c-7cdb-486b-ae10-a59eb6324f28.
[DEPEND] Dependency failed for Swap.
...
[  OK  ] Started Emergency Shell.
[  OK  ] Reached target Emergency Mode.
...
# systemctl --failed
  UNIT                     LOAD   ACTIVE SUB    DESCRIPTION                    
● systemd-sysctl.service   loaded failed failed Apply Kernel Variables         
● systemd-sysusers.service loaded failed failed Create System Users            

LOAD   = Reflects whether the unit definition was properly loaded.
ACTIVE = The high-level unit activation state, i.e. generalization of SUB.
SUB    = The low-level unit activation state, values depend on unit type.

2 loaded units listed. Pass --all to see loaded but inactive units, too.
To show all installed unit files use 'systemctl list-unit-files'.
```

uh, right.  Also, since `journald` didn't start, I think I'm missing useful system logs :-(.  `journalctl` only shows stuff from the initrd.

```
# systemctl list-jobs
JOB UNIT                                 TYPE  STATE  
225 systemd-update-utmp-runlevel.service start waiting
151 systemd-tmpfiles-setup.service       start running
254 machines.target                      start waiting
164 systemd-tmpfiles-setup-dev.service   start running
263 nss-lookup.target                    start waiting
414 systemd-journald.service             start running
161 local-fs-pre.target                  start waiting
241 network.target                       start waiting
255 var-lib-machines.mount               start waiting
141 systemd-udevd.service                start waiting
262 systemd-resolved.service             start waiting
265 auditd.service                       start waiting
278 systemd-networkd.service             start waiting
226 systemd-update-utmp.service          start waiting

14 jobs listed.
```

It doesn't look like we sent useful stuff to dmesg instead either...  at a guess all the useful messages are sitting in the journald socket.  Hum.

```
# dmesg |grep -i udev
[    1.667466] audit: type=1130 audit(1516793679.975:10): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=kernel msg='unit=dracut-pre-udev comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[   24.075129] audit: type=1130 audit(1516793702.384:60): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udev-trigger comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
[  154.394602] audit: type=1130 audit(1516793832.704:83): pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg='unit=systemd-udev-settle comm="systemd" exe="/usr/lib/systemd/systemd" hostname=? addr=? terminal=? res=success'
# dmesg |grep -i rate
[    2.793437] systemd-journal: 29 output lines suppressed due to ratelimiting
[    2.820343] systemd: 256 output lines suppressed due to ratelimiting
```
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `420d2058674b8f0edb6c135c125df0781b87d964` and the full history behind it is present.
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
