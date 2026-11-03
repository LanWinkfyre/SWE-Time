# Locate the commit that introduced this regression

A regression was reported against `zed-industries/zed`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[Linux] Clicking git blame crashes Zed

### Check for existing issues

- [X] Completed

### Describe the bug / provide steps to reproduce it

Open Zed repo in Zed, toggle git blame, click on the git blame entry

Expected: a browser is opened with the relevant commit
Actual: a cryptic panic

```
2024-11-28T23:40:47.200746554+02:00 [ERROR] {
  "thread": "<unnamed>",
  "payload": "there is no reactor running, must be called from the context of a Tokio 1.x runtime",
  "location_data": {
    "file": "/home/ubuntu/.cargo/registry/src/index.crates.io-6f17d22bba15001f/zbus-5.1.1/src/abstractions/executor.rs",
    "line": 189
  },
  "backtrace": [
    "core::panicking::panic_fmt",
    "tokio::runtime::scheduler::Handle::current::panic_cold_display",
    "tokio::runtime::scheduler::Handle::current",
    "zbus::connection::builder::Builder::build_::{{closure}}",
    "ashpd::proxy::Proxy::connection::{{closure}}",
    "ashpd::proxy::Proxy::new_desktop::{{closure}}",
    "ashpd::desktop::open_uri::OpenURIProxy::new::{{closure}}",
    "gpui::platform::linux::platform::open_uri_internal::{{closure}}",
    "async_task::raw::RawTask<F,T,S,M>::run",
    "std::sys::backtrace::__rust_begin_short_backtrace",
    "core::ops::function::FnOnce::call_once{{vtable.shim}}",
    "std::sys::pal::unix::thread::Thread::new::thread_start",
    "start_thread",
    "__GI___clone3"
  ],
  "app_version": "0.165.0",
  "release_channel": "Zed Nightly",
  "os_name": "Linux Wayland",
  "os_version": "fedora 41",
  "architecture": "x86_64",
  "panicked_on": 1732830047200,
  "system_id": "60289f31-72c4-421e-b50a-0dfcbf8574ca",
  "installation_id": "7469252e-15a5-4388-bf97-205fee3b5cf4",
  "session_id": "de92bfd4-3c36-4501-90fc-9e4cbb9edc43"
}
```

Do note that the path in the backtrace is from the build machine:
```
~ ❯ ls /home
alpc
```

### Environment



Linux alpc 6.11.8-300.fc41.x86_64 #1 SMP PREEMPT_DYNAMIC Thu Nov 14 20:37:39 UTC 2024 x86_64 GNU/Linux

LSB Version:	n/a
Distributor ID:	Fedora
Description:	Fedora Linux 41 (Workstation Edition)
Release:	41
Codename:	n/a


### If applicable, attach your `~/Library/Logs/Zed/Zed.log` file to this issue.

<details><summary>Zed.log</summary>

<!-- Click below this line and paste or drag-and-drop your log-->
```

```
<!-- Click above this line and paste or drag-and-drop your log--></details>
```

## What you have

- `/testbed/repo` is a git clone of `zed-industries/zed` truncated just after the regression was
  reported.  `HEAD` is `3458687300e6d226531019738ad0669993b5c17d` and the full history behind it is present.
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
