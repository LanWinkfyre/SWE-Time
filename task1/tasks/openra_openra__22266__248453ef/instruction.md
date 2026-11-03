# Locate the commit that introduced this regression

A regression was reported against `OpenRA/OpenRA`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
D2K crash when entering (escape) menu as spectator in a bots-only game

## System Information

- Operating System:  Arch Linux x86_64
- OpenRA Version:


- OpenRA Mod: D2K (only)
- Source: self-compiled

## Exception log

```
OpenRA engine version {DEV_VERSION}
d2k mod version {DEV_VERSION}
on map 9b23f59b288872d7748dd8b166882e72f412bf56 (Chin Rock by Westwood Studios).
Date: 2025-12-29 15:34:21Z
Operating System: Linux (X64, Unix 6.18.1.1)
Runtime Version: .NET CLR 8.0.22
Installed Language: en (Installed) en (Current) en (Current UI)
Exception of type `System.Reflection.TargetInvocationException`: Exception has been thrown by the target of an invocation.
Inner
  Exception of type `System.Reflection.TargetInvocationException`: Exception has been thrown by the target of an invocation.
  Inner
    Exception of type `System.Reflection.TargetInvocationException`: Exception has been thrown by the target of an invocation.
    Inner
      Exception of type `System.InvalidCastException`: Unable to cast object of type 'OpenRA.Mods.Common.Widgets.LabelWidget' to type 'OpenRA.Mods.Common.Widgets.LabelWithTooltipWidget'.
         at OpenRA.Widgets.Widget.GetOrNull[T](String id) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 612
   at OpenRA.Widgets.Widget.Get[T](String id) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 617
   at OpenRA.Mods.Common.Widgets.Logic.GameInfoStatsLogic..ctor(Widget widget, ModData modData, World world, OrderManager orderManager, WorldRenderer worldRenderer, Action`1 hideMenu, Action closeMenu) in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/Logic/Ingame/GameInfoStatsLogic.cs:line 301
   at System.RuntimeMethodHandle.InvokeMethod(Object target, Void** arguments, Signature sig, Boolean isConstructor)
   at System.Reflection.MethodBaseInvoker.InvokeWithManyArgs(Object obj, BindingFlags invokeAttr, Binder binder, Object[] parameters, CultureInfo culture)
       at System.Reflection.MethodBaseInvoker.InvokeWithManyArgs(Object obj, BindingFlags invokeAttr, Binder binder, Object[] parameters, CultureInfo culture)
   at OpenRA.ObjectCreator.CreateUsingArgs(ConstructorInfo ctor, Dictionary`2 args) in /home/ashley/devel/OpenRA/OpenRA.Game/ObjectCreator.cs:line 136
   at OpenRA.ObjectCreator.CreateObject[T](String className, Dictionary`2 args) in /home/ashley/devel/OpenRA/OpenRA.Game/ObjectCreator.cs:line 101
   at OpenRA.Widgets.Widget.<>c__DisplayClass28_0.<PostInit>b__0(String l) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 322
   at System.Linq.Enumerable.SelectArrayIterator`2.Fill(ReadOnlySpan`1 source, Span`1 destination, Func`2 func)
   at System.Linq.Enumerable.SelectArrayIterator`2.ToArray()
   at System.Collections.Immutable.ImmutableArray.CreateRange[T](IEnumerable`1 items)
   at OpenRA.Widgets.Widget.PostInit(WidgetArgs args) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 322
   at OpenRA.WidgetLoader.LoadWidget(WidgetArgs args, Widget parent, MiniYamlNode node) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/WidgetLoader.cs:line 70
   at OpenRA.WidgetLoader.LoadWidget(WidgetArgs args, Widget parent, String w) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/WidgetLoader.cs:line 43
   at OpenRA.Game.LoadWidget(World world, String id, Widget parent, WidgetArgs args) in /home/ashley/devel/OpenRA/OpenRA.Game/Game.cs:line 169
   at OpenRA.Mods.Common.Widgets.Logic.GameInfoLogic.SetupObjectivesPanel(ButtonWidget objectivesTabButton, Widget objectivesPanelContainer) in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/Logic/Ingame/GameInfoLogic.cs:line 144
   at OpenRA.Mods.Common.Widgets.Logic.GameInfoLogic..ctor(Widget widget, ModData modData, World world, IngameInfoPanel initialPanel, Action`1 hideMenu, Action closeMenu) in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/Logic/Ingame/GameInfoLogic.cs:line 125
   at System.RuntimeMethodHandle.InvokeMethod(Object target, Void** arguments, Signature sig, Boolean isConstructor)
   at System.Reflection.MethodBaseInvoker.InvokeWithManyArgs(Object obj, BindingFlags invokeAttr, Binder binder, Object[] parameters, CultureInfo culture)
     at System.Reflection.MethodBaseInvoker.InvokeWithManyArgs(Object obj, BindingFlags invokeAttr, Binder binder, Object[] parameters, CultureInfo culture)
   at OpenRA.ObjectCreator.CreateUsingArgs(ConstructorInfo ctor, Dictionary`2 args) in /home/ashley/devel/OpenRA/OpenRA.Game/ObjectCreator.cs:line 136
   at OpenRA.ObjectCreator.CreateObject[T](String className, Dictionary`2 args) in /home/ashley/devel/OpenRA/OpenRA.Game/ObjectCreator.cs:line 101
   at OpenRA.Widgets.Widget.<>c__DisplayClass28_0.<PostInit>b__0(String l) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 322
   at System.Linq.Enumerable.SelectArrayIterator`2.Fill(ReadOnlySpan`1 source, Span`1 destination, Func`2 func)
   at System.Linq.Enumerable.SelectArrayIterator`2.ToArray()
   at System.Collections.Immutable.ImmutableArray.CreateRange[T](IEnumerable`1 items)
   at OpenRA.Widgets.Widget.PostInit(WidgetArgs args) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 322
   at OpenRA.WidgetLoader.LoadWidget(WidgetArgs args, Widget parent, MiniYamlNode node) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/WidgetLoader.cs:line 70
   at OpenRA.WidgetLoader.LoadWidget(WidgetArgs args, Widget parent, String w) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/WidgetLoader.cs:line 43
   at OpenRA.Game.LoadWidget(World world, String id, Widget parent, WidgetArgs args) in /home/ashley/devel/OpenRA/OpenRA.Game/Game.cs:line 169
   at OpenRA.Mods.Common.Widgets.Logic.IngameMenuLogic..ctor(Widget widget, ModData modData, World world, Action onExit, WorldRenderer worldRenderer, IngameInfoPanel initialPanel, Dictionary`2 logicArgs) in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/Logic/Ingame/IngameMenuLogic.cs:line 224
   at System.RuntimeMethodHandle.InvokeMethod(Object target, Void** arguments, Signature sig, Boolean isConstructor)
   at System.Reflection.MethodBaseInvoker.InvokeWithManyArgs(Object obj, BindingFlags invokeAttr, Binder binder, Object[] parameters, CultureInfo culture)
   at System.Reflection.MethodBaseInvoker.InvokeWithManyArgs(Object obj, BindingFlags invokeAttr, Binder binder, Object[] parameters, CultureInfo culture)
   at OpenRA.ObjectCreator.CreateUsingArgs(ConstructorInfo ctor, Dictionary`2 args) in /home/ashley/devel/OpenRA/OpenRA.Game/ObjectCreator.cs:line 136
   at OpenRA.ObjectCreator.CreateObject[T](String className, Dictionary`2 args) in /home/ashley/devel/OpenRA/OpenRA.Game/ObjectCreator.cs:line 101
   at OpenRA.Widgets.Widget.<>c__DisplayClass28_0.<PostInit>b__0(String l) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 322
   at System.Linq.Enumerable.SelectArrayIterator`2.Fill(ReadOnlySpan`1 source, Span`1 destination, Func`2 func)
   at System.Linq.Enumerable.SelectArrayIterator`2.ToArray()
   at System.Collections.Immutable.ImmutableArray.CreateRange[T](IEnumerable`1 items)
   at OpenRA.Widgets.Widget.PostInit(WidgetArgs args) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 322
   at OpenRA.WidgetLoader.LoadWidget(WidgetArgs args, Widget parent, MiniYamlNode node) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/WidgetLoader.cs:line 70
   at OpenRA.WidgetLoader.LoadWidget(WidgetArgs args, Widget parent, String w) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/WidgetLoader.cs:line 43
   at OpenRA.Game.LoadWidget(World world, String id, Widget parent, WidgetArgs args) in /home/ashley/devel/OpenRA/OpenRA.Game/Game.cs:line 169
   at OpenRA.Mods.Common.Widgets.Logic.MenuButtonsChromeLogic.OpenMenuPanel(MenuButtonWidget button, WidgetArgs widgetArgs) in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/Logic/Ingame/MenuButtonsChromeLogic.cs:line 120
   at OpenRA.Mods.Common.Widgets.Logic.MenuButtonsChromeLogic.<>c__DisplayClass5_2.<.ctor>b__1() in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/Logic/Ingame/MenuButtonsChromeLogic.cs:line 45
   at OpenRA.Mods.Common.Widgets.ButtonWidget.<.ctor>b__41_9(KeyInput _) in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/ButtonWidget.cs:line 90
   at OpenRA.Mods.Common.Widgets.ButtonWidget.HandleKeyPress(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Mods.Common/Widgets/ButtonWidget.cs:line 154
   at OpenRA.Widgets.Widget.HandleKeyPressOuter(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 466
   at OpenRA.Widgets.Widget.HandleKeyPressOuter(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 462
   at OpenRA.Widgets.Widget.HandleKeyPressOuter(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 462
   at OpenRA.Widgets.Widget.HandleKeyPressOuter(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 462
   at OpenRA.Widgets.Widget.HandleKeyPressOuter(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 462
   at OpenRA.Widgets.Widget.HandleKeyPressOuter(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 462
   at OpenRA.Widgets.Ui.HandleKeyPress(KeyInput e) in /home/ashley/devel/OpenRA/OpenRA.Game/Widgets/Widget.cs:line 150
   at OpenRA.DefaultInputHandler.<>c__DisplayClass3_0.<OnKeyInput>b__0() in /home/ashley/devel/OpenRA/OpenRA.Game/Input/InputHandler.cs:line 40
   at OpenRA.Sync.RunUnsynced[T](Boolean checkSyncHash, World world, Func`1 fn) in /home/ashley/devel/OpenRA/OpenRA.Game/Sync.cs:line 193
   at OpenRA.Sync.RunUnsynced[T](World world, Func`1 fn) in /home/ashley/devel/OpenRA/OpenRA.Game/Sync.cs:line 180
   at OpenRA.DefaultInputHandler.OnKeyInput(KeyInput input) in /home/ashley/devel/OpenRA/OpenRA.Game/Input/InputHandler.cs:line 40
   at OpenRA.Platforms.Default.Sdl2Input.PumpInput(Sdl2PlatformWindow device, IInputHandler inputHandler, Nullable`1 lockedMousePosition) in /home/ashley/devel/OpenRA/OpenRA.Platforms.Default/Sdl2Input.cs:line 241
   at OpenRA.Platforms.Default.Sdl2PlatformWindow.PumpInput(IInputHandler inputHandler) in /home/ashley/devel/OpenRA/OpenRA.Platforms.Default/Sdl2PlatformWindow.cs:line 498
   at OpenRA.Renderer.EndFrame(IInputHandler inputHandler) in /home/ashley/devel/OpenRA/OpenRA.Game/Renderer.cs:line 332
   at OpenRA.Game.RenderTick() in /home/ashley/devel/OpenRA/OpenRA.Game/Game.cs:line 753
   at OpenRA.Game.Loop() in /home/ashley/devel/OpenRA/OpenRA.Game/Game.cs:line 869
   at OpenRA.Game.Run() in /home/ashley/devel/OpenRA/OpenRA.Game/Game.cs:line 920
   at OpenRA.Game.InitializeAndRun(String[] args) in /home/ashley/devel/OpenRA/OpenRA.Game/Game.cs:line 341
   at OpenRA.Launcher.Program.Main(String[] args) in /home/ashley/devel/OpenRA/OpenRA.Launcher/Program.cs:line 46
```


## Replay

No specific replay applicable - UI bug.

## Additional information

1. Enter a game as a spectator of a bots-only game, or open a replay of such a game. (Any map.)
2. Either: press escape, click the on-screen "Options (Esc)" button, or await game completion. (All should trigger the same menu.)
3. Observe crash.

The issue does not seem to reproduce if there is at least one human player.
```

## What you have

- `/testbed/repo` is a git clone of `OpenRA/OpenRA` truncated just after the regression was
  reported.  `HEAD` is `eb09870a103d8f8a2f6fe07aa30085888e93b269` and the full history behind it is present.
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
