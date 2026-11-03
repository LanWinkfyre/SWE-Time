# Locate the commit that introduced this regression

A regression was reported against `OpenRA/OpenRA`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
FrozenActorLayer: Out of sync

Bleed, shroud off, crates off, debug on. Map: http://resource.openra.net/maps/1715/

```
Red Alert Mod at Version {DEV_VERSION}
Operating System: Windows (Microsoft Windows NT 6.1.7601 Service Pack 1)
Runtime Version: .NET CLR 4.0.30319.42000
Exception of type `System.InvalidOperationException`: Out of sync in frame 829: Blame Tick.
 Compare syncreport.log with other players.
   at OpenRA.Network.OrderManager.OutOfSync(Int32 frame, String blame) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Network\OrderManager.cs:line 63
   at OpenRA.Network.OrderManager.CheckSync(Byte[] packet) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Network\OrderManager.cs:line 161
   at OpenRA.Network.OrderManager.<>c__DisplayClass9.<TickImmediate>b__5(Int32 clientId, Byte[] packet) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Network\OrderManager.cs:line 119
   at OpenRA.Network.ReplayRecorderConnection.<>c__DisplayClass3.<Receive>b__2(Int32 client, Byte[] data) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Network\ReplayRecorderConnection.cs:line 95
   at OpenRA.Network.EchoConnection.Receive(Action`2 packetFn) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Network\Connection.cs:line 103
   at OpenRA.Network.ReplayRecorderConnection.Receive(Action`2 packetFn) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Network\ReplayRecorderConnection.cs:line 82
   at OpenRA.Network.OrderManager.TickImmediate() in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Network\OrderManager.cs:line 112
   at OpenRA.Sync.<>c__DisplayClass5.<CheckSyncUnchanged>b__4() in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Sync.cs:line 168
   at OpenRA.Sync.CheckSyncUnchanged[T](World world, Func`1 fn) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Sync.cs:line 185
   at OpenRA.Sync.CheckSyncUnchanged(World world, Action fn) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Sync.cs:line 168
   at OpenRA.Game.InnerLogicTick(OrderManager orderManager) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Game.cs:line 462
   at OpenRA.Game.LogicTick() in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Game.cs:line 507
   at OpenRA.Game.Loop() in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Game.cs:line 631
   at OpenRA.Game.Run() in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Game.cs:line 671
   at OpenRA.Program.Run(String[] args) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Support\Program.cs:line 111
   at OpenRA.Program.Main(String[] args) in d:\Dev\openra_dev\OpenRA\OpenRA.Game\Support\Program.cs:line 39

```
```

## What you have

- `/testbed/repo` is a git clone of `OpenRA/OpenRA` truncated just after the regression was
  reported.  `HEAD` is `33e779f4c0d75366e41400dc98885afd3dbf6db7` and the full history behind it is present.
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
