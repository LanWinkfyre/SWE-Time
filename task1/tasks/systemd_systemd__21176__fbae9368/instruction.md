# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
pid1: memory not aligned enough used for reading RootImages with O_DIRECT

**systemd version the issue has been seen with**


<!-- **NOTE:** Do not submit bug reports about anything but the two most recently released *major* systemd versions upstream! -->
<!--           If there have been multiple stable releases for that major version, please consider updating to a recent one before reporting an issue. -->
<!--           When using a distro package, please make sure that the version reported is meaningful for upstream. -->
<!-- See https://github.com/systemd/systemd-stable/releases for the list of most recent releases. -->
<!-- For older version please use distribution trackers (see https://systemd.io/CONTRIBUTING#filing-issues). -->

**Used distribution**
 > Debian

**Linux kernel version used** (`uname -a`)
<!-- Make sure to enclose the pasted kernel version in `backticks`, so that
     GitHub doesn't convert the `#` character typically included in it into a
     reference to old GitHub issues. -->
 > `5.14.0-3`

**CPU architecture issue was seen on**
 > x86_64

**Expected behaviour you didn't see**
 > Mounting a squashfs image as `RootImage=` is successful

**Unexpected behaviour you saw**
Starting a service fails:
```
Oct 29 00:08:06 systemd[15228]: systemd-networkd.service: Failed to set up mount namespacing: Invalid argument
Oct 29 00:08:06 systemd[15228]: systemd-networkd.service: Failed at step NAMESPACE spawning /lib/systemd/systemd-networkd: Invalid argument
Oct 29 00:08:06 systemd[1]: systemd-networkd.service: Main process exited, code=exited, status=226/NAMESPACE
Oct 29 00:08:06 systemd[1]: systemd-networkd.service: Failed with result 'exit-code'.
Oct 29 00:08:06 systemd[1]: Failed to start Network Configuration.
Oct 29 00:08:06 systemd[1]: systemd-networkd.service: Scheduled restart job, restart counter is at 5.
Oct 29 00:08:06 systemd[1]: Stopped Network Configuration.
```

**Steps to reproduce the problem**
 > …

**Additional program output to the terminal or log subsystem illustrating the issue**

<!-- Please paste relevant program terminal or journal output here, ideally
     when generated in debug mode (try setting the SYSTEMD_LOG_LEVEL=debug
     environment variable). For very long copy/pasted data consider using a
     service like https://gist.github.com/. Where copy/paste is not possible
     (for example early boot or late shutdown), a photo of the screen might do
     too, but text is always much preferred. -->
Excerpt of strace of PID1 failing when starting `systemd-networkd`:
```text
fstat(4, {st_mode=S_IFBLK|0660, st_rdev=makedev(0xfe, 0x18), ...}) = 0
ioctl(4, BLKGETSIZE64, [54525952])      = 0
openat(AT_FDCWD, "/sys/dev/block/254:24", O_RDONLY|O_CLOEXEC) = 3
openat(3, "dm/uuid", O_RDONLY|O_CLOEXEC) = 5
read(5, "LVM-Yugg1eSiCXG0Mruly3MMsgzRGcDsAw8ilggPJxLdtTuHkJAuwSaP2e151VbHpK56\n", 8191) = 69
read(5, "", 8122)                       = 0
close(5)                                = 0
close(3)                                = 0
lseek(4, 54460416, SEEK_SET)            = 54460416
read(4, 0x555f96eaa268, 64)             = -1 EINVAL (Invalid argument)
fsync(4)                                = 0
close(4)                                = 0
openat(AT_FDCWD, "/dev/kmsg", O_WRONLY|O_NOCTTY|O_CLOEXEC) = 3
clock_gettime(CLOCK_MONOTONIC, {tv_sec=36, tv_nsec=197939784}) = 0
writev(3, [{iov_base="<27>", iov_len=4}, {iov_base="systemd", iov_len=7}, {iov_base="[1686]: ", iov_len=8}, {iov_base="systemd-networkd.service: Failed to set up mount namespacing: Invalid argument", iov_len=78}, {iov_base="\n", iov_len=1}], 5) = 98
```
Line
```text
read(4, 0x555f96eaa268, 64)             = -1 EINVAL (Invalid argument)
```
is the problem. Man read(2):

EINVAL fd is attached to an object which is unsuitable for reading; _or the file was opened with the O_DIRECT flag, and either the address specified in buf, the value specified in count, or the file offset is not suitably aligned._

Offset 54460416 (or 0x33f0000) is well aligned and also count 64 looks good to me, so I think the address 0x555f96eaa268 should be more strictly aligned than by 8. Sadly the manual page doesn't tell what exactly is 'suitably aligned'.

I suppose the fix is that `dissect_image()` (or something related) should use `posix_memalign()` to allocate more aligned memory for reading images opened with O_DIRECT. 

The images are raw squashfs without any MBR/GPT partition tables.
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `ff8b7bd6a0d15311889103c49f752b03d4d830a3` and the full history behind it is present.
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
