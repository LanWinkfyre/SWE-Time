# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Performance regression since 4.2-beta1 when calling `TranslationServer.set_locale()` every frame

### Godot version

4.2

### System information

Windows 11

### Issue description

I started a project in Godot 4 and updated Godot and ended up with Godot 4.2dev_6 because this was compatible with the modi_player addon and Glow at the same time. Other Versions either had framrate issues (like the main problem i have now) or the addon not working.

After Godot 4.2 stable came out, I tried to work in my game with this Version and get massive framerate issues (5fps) in the forward+ and mobile renderer, even in an empty scene. I tried turning off hdr / glow and changed other project settings, but nothing works. 
When I change to the Compatibility render I get the maximum amount of frames possible.

I have a Asus Rog Flow X13, Ryzen 7, GTX 1650 with Max-Q Design and a AMD Radeon Graphics 


### Steps to reproduce

its only in this project, no else, but here are the stept I did with the Game.
- Started dev. in Godot 4.0
- Updated to Godot 4.1
- Installed Godot4.2_dev 3 for hdr glow (in 2D)
- changed to Godot 4.2dev6 because of the midi player addon
- now used a backup copy of my game to test Godot 4.2 stable

### Minimal reproduction project

I won't upload my game here, because I'm pretty far in developement.
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `d76c1d0e516fedc535a2e394ab780cac79203477` and the full history behind it is present.
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
