# Locate the commit that introduced this regression

A regression was reported against `OpenRA/OpenRA`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Loading maps in the editor crashes



## System Information

- Operating System:  Linux

- OpenRA Mod: ra
- Source: self-compiled
- Mono version: 6.8.0.105


## Exception log
```
Exception of type `System.IO.InvalidDataException`: Received packet from disconnected client '0'
   at OpenRA.Network.OrderManager.ReceiveOrders(Int32 clientId, ValueTuple`2 orders) in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Network/OrderManager.cs:line 162
   at OpenRA.Network.NetworkConnection.OpenRA.Network.IConnection.Receive(OrderManager orderManager) in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Network/Connection.cs:line 315
   at OpenRA.Sync.<>c__DisplayClass13_0.<RunUnsynced>b__0() in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Sync.cs:line 166
   at OpenRA.Sync.RunUnsynced[T](Boolean checkSyncHash, World world, Func`1 fn) in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Sync.cs:line 190
   at OpenRA.Sync.RunUnsynced(Boolean checkSyncHash, World world, Action fn) in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Sync.cs:line 167
   at OpenRA.Game.InnerLogicTick(OrderManager orderManager) in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Game.cs:line 628
   at OpenRA.Game.LogicTick() in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Game.cs:line 643
   at OpenRA.Game.Loop() in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Game.cs:line 810
   at OpenRA.Game.Run() in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Game.cs:line 863
   at OpenRA.Game.InitializeAndRun(String[] args) in /home/matthias/Entwicklung/OpenRA/OpenRA.Game/Game.cs:line 281
   at OpenRA.Launcher.Program.Main(String[] args) in /home/matthias/Entwicklung/OpenRA/OpenRA.Launcher/Program.cs:line 32
```
```

## What you have

- `/testbed/repo` is a git clone of `OpenRA/OpenRA` truncated just after the regression was
  reported.  `HEAD` is `e0e219793ff7b39bdec98b45fe9f0785d0612956` and the full history behind it is present.
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
