# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
networkd: Interface stuck in configuring state with DHCPv6-PD and `UplinkInterface=:self`

### systemd version the issue has been seen with

254.6

### Used distribution

NixOS 23.11

### Linux kernel version used

6.1.51

### CPU architectures issue was seen on

x86_64, aarch64

### Component

systemd-networkd

### Expected behaviour you didn't see

When requesting a prefix with IPv6 Prefix Delegation and `UplinkInterface=:self`, the WAN interface should enter the `routable (configured)` state after receiving a prefix.

### Unexpected behaviour you saw

 Addresses are successfully configured on all interfaces as usual, but the state never transitions to `configured`.

### Steps to reproduce the problem

I discovered the issue on an `aarch64` host acting as a residential router.  This is the configuration in the VM:

```
[Match]
Name=eth1

[Link]
RequiredForOnline=routable

[Network]
DHCP=ipv6
DHCPPrefixDelegation=true
IPv6AcceptRA=true
IPv6SendRA=false

[DHCPv6]
PrefixDelegationHint=::/48

[DHCPPrefixDelegation]
Announce=false
UplinkInterface=:self
```

The `aarch64` router additionally configures an address with DHCPv4 and otherwise has a similar config.

### Additional program output to the terminal or log subsystem illustrating the issue

[`systemd-networkd` log](https://gist.githubusercontent.com/Majiir/8de6724fddd7f826a28ab65097e7641d/raw/904ba309ad54940d479755d666e8daeb66fa66f3/networkd.log)
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `e6267e832bc865c5e73e9e48b6dba7d1646f8d2e` and the full history behind it is present.
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
