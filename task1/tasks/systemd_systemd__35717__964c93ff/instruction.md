# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
systemd-localed returns old value from PropertiesChanged signal

### systemd version the issue has been seen with

systemd-256.9-2.fc41.x86_64 and git main

### Used distribution

Fedora 41

### Linux kernel version used

6.12.5-200.fc41.x86_64

### CPU architectures issue was seen on

x86_64

### Component

other

### Expected behaviour you didn't see

Setting the locale, e.g. via `localectl`, should emit a D-Bus PropertiesChanged signal containing the new value in `changed_properties`.

### Unexpected behaviour you saw

localed instead returns the old value, and it continues to return that same value for future calls until it's restarted (or it times out). Among other things, this is breaking the GNOME Settings Region panel in multi-user mode.



### Steps to reproduce the problem

* `gdbus monitor -y -d org.freedesktop.locale1`
* `localectl set-locale LC_TIME=fr_FR.UTF-8`

### Additional program output to the terminal or log subsystem illustrating the issue

```sh
$ sudo dbus-monitor --system 'path=/org/freedesktop/locale1'
signal time=1734809485.708661 sender=org.freedesktop.DBus -> destination=:1.4435 serial=4294967295 path=/org/freedesktop/DBus; interface=org.freedesktop.DBus; member=NameAcquired
   string ":1.4435"
signal time=1734809485.708676 sender=org.freedesktop.DBus -> destination=:1.4435 serial=4294967295 path=/org/freedesktop/DBus; interface=org.freedesktop.DBus; member=NameLost
   string ":1.4435"
method call time=1734809493.256189 sender=:1.4436 -> destination=org.freedesktop.locale1 serial=2 path=/org/freedesktop/locale1; interface=org.freedesktop.locale1; member=SetLocale
   array [
      string "LC_TIME=fr_FR.UTF-8"
   ]
   boolean true
method call time=1734809493.323125 sender=:1.101 -> destination=:1.4438 serial=87 path=/org/freedesktop/locale1; interface=org.freedesktop.DBus.Properties; member=GetAll
   string "org.freedesktop.locale1"
method call time=1734809493.323663 sender=:1.125 -> destination=:1.4438 serial=332 path=/org/freedesktop/locale1; interface=org.freedesktop.DBus.Properties; member=GetAll
   string "org.freedesktop.locale1"
signal time=1734809493.618171 sender=:1.4438 -> destination=(null destination) serial=8 path=/org/freedesktop/locale1; interface=org.freedesktop.DBus.Properties; member=PropertiesChanged
   string "org.freedesktop.locale1"
   array [
      dict entry(
         string "Locale"
         variant             array [
               string "LANG=en_US.UTF-8"
               string "LC_TIME=de_DE.UTF-8"
            ]
      )
   ]
   array [
   ]
```
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `7655550a49056dffaf7e834386ff4cc59bfb4f1a` and the full history behind it is present.
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
