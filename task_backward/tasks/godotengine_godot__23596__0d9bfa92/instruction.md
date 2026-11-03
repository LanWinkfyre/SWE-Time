# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
MeshInstance is ignoring it's material property

**Godot version:**


**OS/device including version:**
Ubuntu 18.04, Gtx1060

**Issue description:**
 


**Steps to reproduce:**
1. Create new scene, `MaterialTester.tscn`, with Spatial node as a root.
2. Add new MeshInstance node as a child to this scene.
3. Create new cube mesh In `Mesh` property of the MeshInstance 
4. Create new Spatial material in `Material` property of MeshInstance (not inside the mesh resource)
5. Change albedo color in newly created SpatialMaterial to full red color.
6. Save the scene
7. Quit Godot
8. Turn on Godot, open your `MaterialTester.tscn` scene
9. Notice that the cube is not rendered as red anymore.

**Minimal reproduction project:**
[MaterialTest.zip](https://github.com/godotengine/godot/files/2562920/MaterialTest.zip)
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `43e358205831fbcc5d6d7e8aade5131168d83651` and the full history behind it is present.
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
