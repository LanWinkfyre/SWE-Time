# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
IPv4 network stays in state "configuring" forever

Our CI tests detected a networkd regression in trunk (still worked in 226): With a standard `.network` file like

```
# cat /run/systemd/network/test_eth42.network 
[Match]
Name=test_eth42
[Network]
DHCP=yes
```

the interface now stays in state "configuring" eternally:

```
# networkctl status test_eth42
● 14: test_eth42
       Link File: /lib/systemd/network/99-default.link
    Network File: /run/systemd/network/test_eth42.network
            Type: ether
           State: routable (configuring)
          Driver: veth
      HW Address: 5e:4b:19:a5:64:72
             MTU: 1500
         Address: 192.168.5.127
                  fe80::5c4b:19ff:fea5:6472
         Gateway: 192.168.5.1
             DNS: 192.168.5.1
```

The interface is actually fully configured, I'm not quite sure yet what it's still waiting on. Journal output from the point when networkd starts:

```
Sep 24 10:49:00 debian systemd[1]: Started Network Service.
Sep 24 10:49:00 debian systemd-udevd[4524]: Could not generate persistent MAC address for router_eth42: No such file or directory
Sep 24 10:49:00 debian systemd-udevd[4525]: Could not generate persistent MAC address for test_eth42: No such file or directory
Sep 24 10:49:00 debian kernel: IPv6: ADDRCONF(NETDEV_UP): router_eth42: link is not ready
Sep 24 10:49:00 debian kernel: IPv6: ADDRCONF(NETDEV_CHANGE): router_eth42: link becomes ready
Sep 24 10:49:00 debian systemd-networkd[4522]: test_eth42: Gained carrier
Sep 24 10:49:00 debian systemd-networkd[4522]: router_eth42: Gained carrier
Sep 24 10:49:00 debian systemd-timesyncd[3262]: Synchronized to time server 78.46.76.100:123 (0.debian.pool.ntp.org).
Sep 24 10:49:01 debian systemd-timesyncd[3262]: Network configuration changed, trying to establish connection.
Sep 24 10:49:01 debian systemd-timesyncd[3262]: Synchronized to time server 78.46.76.100:123 (0.debian.pool.ntp.org).
Sep 24 10:49:02 debian systemd-timesyncd[3262]: Network configuration changed, trying to establish connection.
Sep 24 10:49:02 debian systemd-timesyncd[3262]: Synchronized to time server 78.46.76.100:123 (0.debian.pool.ntp.org).
Sep 24 10:49:05 debian systemd-networkd[4522]: test_eth42: DHCPv4 address 192.168.5.127/24 via 192.168.5.1
Sep 24 10:49:05 debian systemd-networkd[4522]: test_eth42: Not connected to system bus, ignoring transient hostname.
Sep 24 10:49:05 debian systemd-timesyncd[3262]: Network configuration changed, trying to establish connection.
Sep 24 10:49:05 debian systemd-timesyncd[3262]: Synchronized to time server 78.46.76.100:123 (0.debian.pool.ntp.org).
```

I'll run a bisect and further investigations, but want to flag this for the upcoming 227 release.
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `56c581598389739ba2a97baf896ea9277c278a1d` and the full history behind it is present.
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
