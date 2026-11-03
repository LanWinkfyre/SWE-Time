# Recover the symbolic verification state this change produces

A regression report was filed against `giampaolo/psutil`.  The report is quoted verbatim below.

## Report

```
[Windows] `boot_time()` goes off in case of system suspension

Test:

1) run:

```python
import psutil

def to_human(secs):
    return datetime.datetime.fromtimestamp(secs).strftime("%Y-%m-%d %H:%M:%S")

print(to_human(psutil.boot_time()))
```

Prints:

```
2025-04-09 11:20:28
```
2) suspend the system for some minutes (note: in my case I suspended the VirtualBox machine; not sure if it's the same)
3) re-run the script; it prints

```
2025-04-09 11:23:00
```

----

The problems comes from `GetTickCount64`. From [MS doc](https://learn.microsoft.com/en-us/previous-versions/windows/embedded/ms885645(v=msdn.10)?redirectedfrom=MSDN):

> This function returns the number of milliseconds since the device booted, excluding any time that the system was suspended.

A reliable way to get system time via cmdline is:

```
$ net stats workstation | find "Statistics since"
Statistics since 4/9/2025 11:20:28 AM
```

In C code:

```c
#define EPOCH_DIFF_SECONDS 11644473600LL  // seconds from 1601 to 1970

// Return a Python float representing the system uptime expressed in
// seconds since the epoch. The returned value never changes,
// regardless of suspend, hybernate or updates to the system clock.
psutil_boot_time(PyObject *self, PyObject *args) {
    LPBYTE buf = NULL;
    time_t unix_time;
    ULONGLONG filetime;
    NET_API_STATUS status;

    status = NetStatisticsGet(NULL, (LPTSTR)L"LanmanWorkstation", 0, 0, &buf);
    if (status != NERR_Success) {
        PyErr_SetFromWindowsErr(status);
        return NULL;
    }

    STAT_WORKSTATION_0 *stats = (STAT_WORKSTATION_0*)buf;

    // Convert FILETIME (100-ns intervals since 1601) to time_t (secs
    // since 1970).
    filetime = stats->StatisticsStartTime.QuadPart;
    unix_time = (time_t)((filetime / 10000000) - EPOCH_DIFF_SECONDS);

    NetApiBufferFree(buf);
    return Py_BuildValue("d", (double)unix_time);
}
```

The returned value never changes,  regardless of hybernate/suspend, and **also in case of system clock updates**. On all other platforms a systems a system clock update results in `boot_time()` returning a different value, so I'm not sure if we want to stick with this solution.

# APIs

`GetTickCount64`

* basically it's the "uptime", meaning the number of secs since boot
* takes freeze into account? NO
* takes system clock update into account? YES (since it can be combined with `time.time()`)

----

`QueryInterruptTime`

* basically the same as `GetTickCount64` but takes freeze into account
* Requires Windows 7+
* 
----

`NetStatisticsGet`

* takes freeze into account? YES
* takes system clock update into account? NO (it's a static value set on boot)

----

`NtQuerySystemInformation(SystemTimeOfDayInformation)`

* don't know anything yet

----

#  CLI methods to get boot time

```
$ net stats workstation
...
Statistics since 4/9/2025 3:37:56 PM
```

* takes freeze into account? YES (most likely uses ` NetStatisticsGet`)
* takes system clock update into account? NO

----

```
$ systeminfo | find "System Boot Time:"
System Boot Time:          4/9/2025, 8:38:38 PM
```

* takes freeze into account? NO
* takes system clock update into account? DON'T KNOW

----

```
> wmic os get lastbootuptime
LastBootUpTime
20250409203838.100894+120
```

* takes freeze into account? NO
* takes system clock update into account? DON'T KNOW
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `acd30524a0671fddba84c6ebd047657cbec2a774`.  There
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
{"case_id": "giampaolo_psutil__2552__acd3052",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
