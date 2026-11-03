# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
systemd-journald: very large virt memory leak (heap)

Debian 240-4

VSS/VSIZE growing very rapidly without bound.

https://github.com/systemd/systemd/issues/9141?fbclid=IwAR0ji5RLdD6bxZH0erUdl2IUymVWvrONdWmUYm1qgfvK2ZyMX5SVlOMVE3U#issuecomment-454126686

https://bugzilla.redhat.com/show_bug.cgi?id=1665931
```
$ sudo pmap --extended $(pidof systemd-journald) | sort -rnk 2 | head
0000563884697000 7910112   33504   33504 rw---   [ anon ]
00007f6950a81000    8192    7432    7432 rw-s- system@2bbaf66c15df446c9f33ec3169b8d32a-0000000000000001-00057fc6d38900f9.journal
00007f6950080000    8192    6992    6992 rw-s- system@2bbaf66c15df446c9f33ec3169b8d32a-0000000000000001-00057fc6d38900f9.journal
00007f694f880000    8192    7272    7272 rw-s- system@2bbaf66c15df446c9f33ec3169b8d32a-0000000000000001-00057fc6d38900f9.journal
00007f694f080000    8192    7388    7388 rw-s- system@2bbaf66c15df446c9f33ec3169b8d32a-0000000000000001-00057fc6d38900f9.journal
00007f694e880000    8192    6616    6616 rw-s- system@2bbaf66c15df446c9f33ec3169b8d32a-0000000000000001-00057fc6d38900f9.journal
00007f694e080000    8192    6896    6896 rw-s- system@2bbaf66c15df446c9f33ec3169b8d32a-0000000000000001-00057fc6d38900f9.journal
00007f694d0b5000    8192    3368    3368 rw-s- system.journal
00007f694c8b5000    8192       8       8 rw---   [ anon ]
00007f694d8b5000    7980    4308    4308 rw-s- system@2bbaf66c15df446c9f33ec3169b8d32a-0000000000000001-00057fc6d38900f9.journal
```
-XX says its heap
```
$ sudo pmap -XX $(pidof systemd-journald)
9265:   /lib/systemd/systemd-journald
         Address Perm   Offset Device   Inode    Size KernelPageSize MMUPageSize   Rss   Pss Shared_Clean Shared_Dirty Private_Clean Private_Dirty Referenced Anonymous LazyFree AnonHugePages ShmemPmdMapped Shared_Hugetlb Private_Hugetlb Swap SwapPss Locked              VmFlags Mapping
....
    563884697000 rw-p 00000000  00:00       0 7946976              4           4 33652 33652            0            0             0         33652      30888     33652        0             0              0              0               0    0       0      0    rd wr mr mw me ac [heap]
```
Grows without bound until it is restarted
```
~$ sudo ps axuk-vsz | head
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root      9265  0.0  1.0 8005204 89416 ?       Ss   Jan18   0:09 /lib/systemd/systemd-journald
mysql     1025  0.3  2.5 1867820 207312 ?      Sl   Jan18   5:47 /usr/sbin/mysqld --daemonize --pid-file=/run/mysqld/mysqld.pid
nyet       987  0.2  0.2 1016720 23752 ?       Ssl  Jan18   4:14 /usr/bin/rslsync --config /etc/resilio-sync/nyet.conf
root       938  0.2  0.3 848372 24728 ?        Ssl  Jan18   3:59 /usr/bin/python3 /usr/bin/fail2ban-server -xf start
clamav     710  0.0  7.4 842544 604508 ?       Ssl  Jan18   1:04 /usr/sbin/clamd --foreground=true
bind       966  0.0  0.7 446904 60704 ?        Ssl  Jan18   0:46 /usr/sbin/named -u bind
nobody     912  0.0  0.0 409888  3296 ?        Ssl  Jan18   0:19 /usr/bin/memcached -m 64 -p 11211 -u nobody -l 127.0.0.1
root       699  0.0  0.1 403960 11484 ?        Ssl  Jan18   0:00 /usr/lib/udisks2/udisksd
_graphi+ 16835  0.0  0.5 389808 45980 ?        Sl   00:00   0:03 (wsgi:_graphite)  -k start
```
More importantly, you can see it was fine until I "upgraded" systemd on around Jan 14
```
2019-01-14 06:26:04 upgrade systemd:amd64 240-3 240-4
```
![memory-pinpoint 1547269562 1547960762](https://user-images.githubusercontent.com/1088639/51435555-9ecfc280-1c2e-11e9-8464-9a1955bd8f18.png)


Here are my first results:
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `8464d9e0dc506538fd0f2d1d667966750cb9cf30` and the full history behind it is present.
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
