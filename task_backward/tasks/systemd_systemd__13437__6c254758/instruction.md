# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
logind: 243~rc2 break VT/tty switching on Fedora 31

On a fully up2date Fedora 31 system with systemd 243~rc2 VT/tty switching is broken.

To reproduce:

1. Take fully up2date default Fedora 31 workstation install (so using the GNOME desktop in Wayland mode)
2. Log in
3. Switch to VT6 by pressing CTRL + ALT + F6
4. Now try to switch to VT5 with either ALT + F6 or with ALT + cursor-left
5. Notice how the VT is now stuck and stays at VT6, switching back to the GNOME user session by pressing ALT+F2 is also broken

Downgrading systemd (and only systemd) to 242-6.git9d34e79.fc31 fixes things, after this switching to VT5 or back to the GNOME user session works normally.

This was originally reported against gnome-shell but after debugging this it appears to be a systemd bug, see here for the gnome-shell issue: https://gitlab.gnome.org/GNOME/gnome-shell/issues/1549

I couldn't figure out what is going on based on the logs, because they are full of various warnings and errors, and I don't know what is relevant. In addition, even with systemd-242, switching to a tty and back gnome-session doesn't work: Xwayland crashes and the session is aborted. So things were already broken with v242, and they are slightly more broken with v243-rc2.

Nevertheless, I settled on the following bisect strategy: is is possible to switch from gdm *login prompt* to tty and back (and does this happen with normal speed)? Bisecting on this gives the following answer:
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `f6301bdc81c7aca37fb21da877900ad0f9fbd49c` and the full history behind it is present.
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
