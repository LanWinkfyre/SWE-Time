# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
C: discontinue usage of `sprintf`

`sprintf` is generally discouraged because it does not check the size of the destination buffer, meaning it could potentially lead to buffer overflows.

There's 43 occurrences of `sprintf` within psutil code. All of these should be replaced with `snprintf` or similar.

```
~/svn/psutil {master}$ grep -r sprintf . | wc -l
43
~/svn/psutil {master}$ grep -r sprintf .
./psutil/arch/netbsd/proc.c:    if (asprintf(&buf, "/proc/%d/cwd", (int)pid) < 0) {
./psutil/arch/windows/sys.c:            sprintf_s(
./psutil/arch/windows/init.c:    sprintf(fullmsg, "(originated from %s)", syscall);
./psutil/arch/windows/disk.c:        sprintf_s(szDevice, MAX_PATH, "\\\\.\\PhysicalDrive%d", devNum);
./psutil/arch/windows/disk.c:        sprintf_s(szDeviceDisplay, MAX_PATH, "PhysicalDrive%i", devNum);
./psutil/arch/windows/proc_info.c:        sprintf(fullmsg, "%s -> ERROR_NOACCESS", syscall);
./psutil/arch/windows/proc_info.c:    sprintf(fullmsg, "%s -> %lu (%s)", syscall, err, strerror(err));
./psutil/arch/windows/net.c:                    sprintf_s(
./psutil/arch/windows/net.c:                    sprintf_s(
./psutil/arch/windows/net.c:            sprintf_s(descr, MAX_PATH, "%wS", pCurrAddresses->Description);
./psutil/arch/freebsd/proc.c:        sprintf(
./psutil/arch/freebsd/sensors.c:    sprintf(sensor, "dev.cpu.%d.temperature", core);
./psutil/arch/freebsd/sensors.c:    sprintf(sensor, "dev.cpu.%d.coretemp.tjmax", core);
./psutil/arch/freebsd/cpu.c:    sprintf(sensor, "dev.cpu.%d.freq", core);
./psutil/arch/freebsd/cpu.c:    sprintf(sensor, "dev.cpu.%d.freq_levels", core);
./psutil/arch/all/init.c:    sprintf(msg, "assume no such process (originated from %s)", syscall);
./psutil/arch/all/init.c:    sprintf(msg, "assume access denied (originated from %s)", syscall);
./psutil/arch/all/init.c:    sprintf(fullmsg, "(originated from %s)", syscall);
./psutil/arch/all/init.c:    sprintf(fullmsg, "%s (originated from %s)", strerror(errno), syscall);
./psutil/arch/bsd/init.c:    sprintf(fullmsg, "(originated from %s: %s)", syscall, errbuf);
./psutil/arch/bsd/proc.c:    sprintf(str, "%s", kp.ki_comm);
./psutil/arch/bsd/proc.c:    sprintf(str, "%s", kp.p_comm);
./psutil/arch/bsd/proc.c:                sprintf(
./psutil/arch/bsd/proc.c:                sprintf(errbuf, "kvm_getenvv(pid=%ld)", pid);
./psutil/arch/posix/net.c:            sprintf(ptr, "%02x:", data[n] & 0xff);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/psinfo", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/psinfo", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/psinfo", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/status", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/lpsinfo", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/cred", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/usage", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/usage", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/lwp/%i/lwpstatus", procfs_path, pid, tid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/status", procfs_path, pid);
./psutil/arch/sunos/proc.c:    sprintf(path, "%s/%i/xmap", procfs_path, pid);
./psutil/arch/sunos/proc.c:        sprintf(
./psutil/_psutil_aix.c:    sprintf(path, "%s/%i/psinfo", procfs_path, pid);
./psutil/_psutil_aix.c:        sprintf(path, "%s/%i/status", procfs_path, pid);
./psutil/_psutil_aix.c:    sprintf(path, "%s/%i/psinfo", procfs_path, pid);
./psutil/_psutil_aix.c:    sprintf(path, "%s/%i/status", procfs_path, pid);
./psutil/_psutil_aix.c:    sprintf(path, "%s/%i/cred", procfs_path, pid);
./HISTORY.rst:  ``GetLastError()`` called after ``sprintf()``.  (patch by alxchk)
```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1ba3cf53a89d0e097848933a4e751e7cbce40be7`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "giampaolo_psutil__2669__1ba3cf5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
