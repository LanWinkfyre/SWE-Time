# Locate the commit that introduced this regression

A regression was reported against `OpenRA/OpenRA`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Skirmish map generator crashes

In RA when you select the 3 players, the game immediatelly crashes

```
Unhandled exception. System.ArgumentNullException: Value cannot be null. (Parameter 'key')
   at System.Collections.Generic.Dictionary`2.FindValue(TKey key)
   at System.Collections.Generic.Dictionary`2.get_Item(TKey key)
   at OpenRA.Mods.Common.Widgets.Logic.MapGeneratorLogic.<>c__DisplayClass36_1.<RefreshSettings>b__18(String v) in /OpenRA/OpenRA.Mods.Common/Widgets/Logic/MapGeneratorLogic.cs:line 360
   at OpenRA.Primitives.CachedTransform`2.Update(T input) in /OpenRA/OpenRA.Game/Primitives/CachedTransform.cs:line 35
   at OpenRA.Mods.Common.Widgets.Logic.MapGeneratorLogic.<>c__DisplayClass36_8.<RefreshSettings>b__19() in /OpenRA/OpenRA.Mods.Common/Widgets/Logic/MapGeneratorLogic.cs:line 362
   at OpenRA.Mods.Common.Widgets.ButtonWidget.Draw() in /OpenRA/OpenRA.Mods.Common/Widgets/ButtonWidget.cs:line 240
```

I did a bisect.





Only appears to be the lobby-based map generator. Trying 3 players in the map editor has no crash.
```

## What you have

- `/testbed/repo` is a git clone of `OpenRA/OpenRA` truncated just after the regression was
  reported.  `HEAD` is `c588c3ef8dd108677a5c3143cbd0810bb5969608` and the full history behind it is present.
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
