# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
play_backwards() fails to start from end and freezes in 4.6-dev3 (regression from dev2)

### Tested versions

- Reproducible in Godot 4.6 dev 3
- Not reproducible in Godot 4.6 dev 2

### System information

Godot v4.6.dev3 - macOS Tahoe (26.0.1) - Multi-window, 1 monitor - OpenGL 3 (Compatibility) - Apple M4 Pro - Apple M4 Pro (14 threads) - 24.00 GiB memory

### Issue description

The following issue came up in Godot 4.6 dev 3. It was working fine in Godot 4.6 dev 2:

When playing an animation forward and then in a callback reacting to the animation_finished signal playing it backwards, the playback freezes. This is a regression from dev 2.

A workaround is to place the pointer to the end before playing backwards: $AnimationPlayer.seek($AnimationPlayer.current_animation_length, true)


### Steps to reproduce

Play an animation forward an play it backwards immediately when finished. See MRP.



### Minimal reproduction project (MRP)

[mrp-play_backwards.zip](https://github.com/user-attachments/files/23431859/mrp-play_backwards.zip)

```gdscript
extends Node2D


func _ready() -> void:
	var anim = $AnimationPlayer.get_animation("idle")
	if anim:
		var animlen = anim.length
		print("idle length:", animlen)
		
	$AnimationPlayer.play("idle")


func _on_animation_player_animation_finished(anim_name: StringName) -> void:
	print("done '%s'" % anim_name)
	print("starting backwards '%s'" % anim_name)
	# $AnimationPlayer.seek(7.0, true) # FIXME: This is needed in order to start playing backwards.
	$AnimationPlayer.play_backwards("idle")


func _on_animation_player_animation_started(anim_name: StringName) -> void:
	print("started '%s'" % anim_name)

```

Expected result:

```
idle length:7.0
started 'idle'
done 'idle'
starting backwards 'idle'
started 'idle'
done 'idle'
starting backwards 'idle'
started 'idle'
```
(*continues endlessly*)


Actual result in 4.6 dev 3:

```
idle length:7.0
started 'idle'
done 'idle'
starting backwards 'idle'
```
(*animation freezes*)
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `6fd949a6dcbda94140200633394f2b4b99de8f6f` and the full history behind it is present.
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
