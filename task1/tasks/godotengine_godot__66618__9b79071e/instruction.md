# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Vulkan: LightmapGI not visible in 4.0.beta2

### Godot version

4.0.beta2

### System information

Windows 10, Vulkan renderer, Nvidia RTX 3060 ti

### Issue description

When I use a baked LightmapGI node, it seems to just render purely black lightmap textures.
![image](https://user-images.githubusercontent.com/25652538/193129679-eade7117-5016-4966-adf2-08a02d118cac.png)
However, the lightmap texture appears to be baking correctly.
![lightmap_test_scene](https://user-images.githubusercontent.com/25652538/193130049-09e0ec09-29bf-4bb0-953f-a06f9fb50974.png)
This example is with an imported .glb blender with what appear to be properly generated lightmap UVs, too.

### Steps to reproduce

- Import a model.
- Set it to import with lightmap UVs and reimport.
- Place it in a scene with a `DirectionalLight3D` and a `LightmapGI`.
- Bake the lightmaps.

### Minimal reproduction project

[lightmap_bug.zip](https://github.com/godotengine/godot/files/9678734/lightmap_bug.zip)




Fix incoming
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `7c7a86f0fd0c1ae94099f2c1fdd878ab60dcb077` and the full history behind it is present.
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
