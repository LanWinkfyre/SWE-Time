# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Main process exits on reload if `ExecReload` command is failing.

**systemd version the issue has been seen with**
> 239

<!-- **NOTE:** Do not submit bug reports about anything but the two most recently released systemd versions upstream! -->
<!-- For older version please use distribution trackers (see https://github.com/systemd/systemd/blob/master/docs/CONTRIBUTING.md#filing-issues). -->

**Used distribution**
 > Debian Stretch (with stretch-backports enabled in order to get v239)
```
Distributor ID: Debian
Description:    Debian GNU/Linux 9.6 (stretch)
Release:        9.6
Codename:       stretch
```

**Expected behaviour you didn't see**
 > After doing a `systemctl reload apache2` with a bad configuration, apache2 processes should be still running.

**Unexpected behaviour you saw**
 > After doing a `systemctl reload apache2` with a bad configuration, the apache2 main process is killed somehow and apache2 is not running anymore:
```Dec 21 13:02:59 debian-stretch apachectl[1320]: The Apache error log may have more information.
Dec 21 13:02:59 debian-stretch systemd[1]: apache2.service: Control process exited, code=exited status=1
Dec 21 13:02:59 debian-stretch systemd[1]: apache2.service: Failed with result 'exit-code'.
Dec 21 13:02:59 debian-stretch systemd[1]: Reload failed for The Apache HTTP Server.
```

**Steps to reproduce the problem**
1. Install apache2: 
```
apt install apache2
```
2. Check for apache2 processes running:
```
# ps --forest -o user,pid,ppid,command -C apache2
USER       PID  PPID COMMAND
root      1226     1 /usr/sbin/apache2 -k start
www-data  1227  1226  \_ /usr/sbin/apache2 -k start
www-data  1228  1226  \_ /usr/sbin/apache2 -k start
#
```

2. Set bogus directive somewhere in apache2 configuration:
```
echo "-bogus-configuration-" > /etc/apache2/conf-enabled/bogus.conf
```
3. Reload `apache2.service`:
```
systemctl reload apache2.service
```
4. check again for apache2 processes running:
```
# ps --forest -o user,pid,ppid,command -C apache2
USER       PID  PPID COMMAND
#
```
5. The status of `apache2.service` states that control process exited and apache2 main process has exited as well.

**Notes**
This is the current service unit shipped with `apache2` package:
```# /lib/systemd/system/apache2.service
[Unit]
Description=The Apache HTTP Server
After=network.target remote-fs.target nss-lookup.target

[Service]
Type=forking
Environment=APACHE_STARTED_BY_SYSTEMD=true
ExecStart=/usr/sbin/apachectl start
ExecStop=/usr/sbin/apachectl stop
ExecReload=/usr/sbin/apachectl graceful
PrivateTmp=true
Restart=on-abort

[Install]
WantedBy=multi-user.target
```

I think it's worth noting that doing an `apachectl -k graceful` do not kill the current running apache2 processes but only raise a return code != 0 if configuration is wrong.

```
# apachectl -k graceful; echo "APACHECTL_RETCODE=$?";ps --forest -o user,pid,ppid,command -C apache2
AH00526: Syntax error on line 1 of /etc/apache2/conf-enabled/bogus.conf:
Invalid command '-bogus-configuration-', perhaps misspelled or defined by a module not included in the server configuration
Action '-k graceful' failed.
The Apache error log may have more information.
APACHECTL_RETCODE=1
USER       PID  PPID COMMAND
root      1361     1 /usr/sbin/apache2 -k start
www-data  1362  1361  \_ /usr/sbin/apache2 -k start
www-data  1363  1361  \_ /usr/sbin/apache2 -k start
```

It seems weird actually since I used to do many reload with systemd in the past 2 years and never experienced this as far as i can recall ... :thinking: 

Also, this may be related to #2175 but I'm not sure if it's relevant.

I'm seeing the same thing with another service (icinga2) and systemd 239. Strace shows PID 1 killing it with SIGTERM and I can see that using `ExecReload=-` makes it behave as expected (ExecReload failing doesn't cause the main PID to be killed).
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `b72200a8a1c01ad74bdac45a0ccb3a8a6cb2e6aa` and the full history behind it is present.
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
