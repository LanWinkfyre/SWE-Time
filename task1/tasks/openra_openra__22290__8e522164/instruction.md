# Locate the commit that introduced this regression

A regression was reported against `OpenRA/OpenRA`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Map editor can create disordered player definitions

## Issue Summary

The order of (`Multi*`) player definitions should be sorted. E.g., Neutral, Creeps, Multi0, Multi1, ...

However, operations which update multiple mpspawns at once in the map editor (such as via map generation, copy-paste, deletion, undo/redo) can result in the map's player definitions becoming unsorted. (E.g., Neutral, Creeps, Multi1, Multi0.) This disorder becomes persistent, requiring manual MiniYaml intervention to fix.

This bad ordering can later result in crashes. See #22289.

Version Information:


  - (Not present in an official release.)

Code observation: A dictionary is used internally to hold player definitions (see `MapPlayers`), which doesn't provide adequate ordering guarantees.

## Reproduction

1. Open map editor.
2. Go to the "Experimental RMG" tool.
3. Click generate **twice**. (The first time creates a normal ordering, but the second time must remove the old players before re-adding them.)
4. Save the map.
5. Inspect the map's MiniYaml.

Observe the player definitions are out of order (Multi1 before Multi0).

## Expected behavior

Player definitions should be in the correct order.

## Screenshots / Screen recordings / Replays

N/A
```

## What you have

- `/testbed/repo` is a git clone of `OpenRA/OpenRA` truncated just after the regression was
  reported.  `HEAD` is `2c0a4f5873054daac4b6f2749620b17a5a19bbea` and the full history behind it is present.
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
