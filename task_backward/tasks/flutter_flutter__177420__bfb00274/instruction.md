# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
`BackdropFilterLayer` might use incorrect clip on iOS simulator

**Edit by @dkwingsmt :**

This bug only occurs on iOS simulator. Not on iOS device, not macOS, and is likely unrelated with impeller.

For a minimal repro and a more technical description of the bug, see https://github.com/flutter/flutter/issues/177420#issuecomment-3775486926. 

------

**Original issue:** 

**Title: A blur on the route behind a CupertinoSheetRoute will go outside of the rounded edge**

If there is a blur effect at the top of the page behind a CupertinoSheetRoute over a scrollable widget, the blur will go outside of the rounded edge clipping once the sheet transition is completely at rest.

https://github.com/user-attachments/assets/d3cae61a-8545-4a96-9964-fd54c50fcce4

The necessary conditions for this seems to be:
1. The app is running on iOS or android. This does not reproduce on macOS or android with Impeller turned off, so this is likely an Impeller only issue.
2. The page contains a scrolling widget that reaches the top of the page.
3. At the top of the page, there is a blur effect layered over the scrolling widget.
4. CupertinoSheetRoute is opened.

Cupertino navbars will automatically apply a blur if their background color has some transparency in it, so the above behavior can be seen if the route before the CupertinoSheetRoute has a navbar like this:

```dart
navigationBar: const CupertinoNavigationBar.large(
  largeTitle: Text('Sheet Example'),
  backgroundColor: Color(0x85F9F9F9),
  automaticBackgroundVisibility: false,
)
```

<details><summary>Code sample</summary>

```dart
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_localizations/flutter_localizations.dart';

void main() {
  runApp(const CupertinoSheetApp());
}

class CupertinoSheetApp extends StatelessWidget {
  const CupertinoSheetApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      title: 'Cupertino Sheet',
      home: HomePage(),
      theme: CupertinoThemeData(
        brightness: Brightness.light,
      ),
      localizationsDelegates: [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: const CupertinoNavigationBar.large(
        largeTitle: Text('Sheet Example'),
        backgroundColor: Color(0x85F9F9F9),
        transitionBetweenRoutes: false,
        automaticBackgroundVisibility: false,
      ),
      child: ListView.builder(
        itemCount: 50,
        itemBuilder: (context, index) {
          return CupertinoListTile(
            onTap: () {
              Navigator.of(context).push(
                CupertinoSheetRoute<void>(
                  builder: (BuildContext context) => const _SheetScaffold(),
                ),
              );
            },
            title: Text('Test $index'),
            trailing: Material(
              type: MaterialType.transparency,
              child: PopupMenuButton(
                itemBuilder: (context) {
                  return [
                    const PopupMenuItem(child: Text('Item 1')),
                    const PopupMenuItem(child: Text('Item 2')),
                  ];
                },
              ),
            ),
          );
        },
      ),
    );
  }
}

class _SheetScaffold extends StatelessWidget {
  const _SheetScaffold();

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: const CupertinoNavigationBar.large(
        largeTitle: Text('Sheet Example'),
        backgroundColor: Color(0x85F9F9F9),
        transitionBetweenRoutes: false,
      ),
      child: ListView.builder(
        itemCount: 50,
        itemBuilder: (context, index) {
          return CupertinoListTile(
            onTap: () {
              Navigator.of(context).push(
                CupertinoSheetRoute<void>(
                  builder: (BuildContext context) => const _SheetScaffold(),
                ),
              );
            },
            title: Text('Test $index'),
            trailing: Material(
              type: MaterialType.transparency,
              child: PopupMenuButton(
                itemBuilder: (context) {
                  return [
                    const PopupMenuItem(child: Text('Item 1')),
                    const PopupMenuItem(child: Text('Item 2')),
                  ];
                },
              ),
            ),
          );
        },
      ),
    );
  }
}

```
</details>

<details><summary>Code sample without CupertinoNavigationBar</summary>

```dart
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import 'dart:ui' show ImageFilter;

void main() {
  runApp(const CupertinoSheetApp());
}

class CupertinoSheetApp extends StatelessWidget {
  const CupertinoSheetApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const CupertinoApp(
      title: 'Cupertino Sheet',
      home: BlurredHomePage(
        child: HomePage(),
      ),
      theme: CupertinoThemeData(
        brightness: Brightness.light,
      ),
    );
  }
}

class BlurredHomePage extends StatelessWidget {
  const BlurredHomePage({super.key, required this.child});

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return Stack(
      fit: StackFit.expand,
      children: [
        child,
        BackdropFilter(
          // enabled: false,
          filter: ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
          child: DecoratedBox(
            decoration: BoxDecoration(
                color: CupertinoColors.systemBackground.withAlpha(150)),
            child: SizedBox.expand(
                child: Center(
              child: CupertinoButton(
                child: Text('Open Sheet'),
                onPressed: () {
                  Navigator.of(context).push(
                    CupertinoSheetRoute<void>(
                      builder: (BuildContext context) => const _SheetScaffold(),
                    ),
                  );
                },
              ),
            )),
          ),
        ),
      ],
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      child: SingleChildScrollView(
        child: Column(
          children: <Widget>[
            Container(
              height: 500,
              color: Colors.amber[600],
              child: const Center(child: Text('Entry A')),
            ),
            Container(
              height: 500,
              color: Colors.amber[500],
              child: const Center(child: Text('Entry B')),
            ),
            Container(
              height: 500,
              color: Colors.amber[100],
              child: const Center(child: Text('Entry C')),
            ),
          ],
        ),
      ),
    );
  }
}

class _SheetScaffold extends StatelessWidget {
  const _SheetScaffold();

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      child: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            const Text('CupertinoSheetRoute'),
            CupertinoButton.filled(
              onPressed: () {
                Navigator.of(context).maybePop();
              },
              child: const Text('Close sheet'),
            ),
          ],
        ),
      ),
    );
  }
}
```

</details>

The blur going outside of the rounded border can happen as well on the sheet itself. It's different from the one applied by the previous route in that the blur leaking happens at all points of the transition, not just when the transition is fully completed.

https://github.com/user-attachments/assets/f94f050d-1cf8-4a81-be05-75cbfb28de89

The transition that wraps the previous route contains a ScaleTransition. Removing the filterQuality makes the blur leak randomly during the transition.

https://github.com/user-attachments/assets/3c3f5226-1770-4675-9ab5-439d466537ec

The blur will also still leak outside of the clip on the top route when the previous route transition is disabled.

https://github.com/user-attachments/assets/796b361b-9487-41b8-bcb8-a6525ea7e92b

 The code for the transition that wraps the previous page can be found at CupertinoSheetTransition.delegateTransition
https://github.com/flutter/flutter/blob/master/packages/flutter/lib/src/cupertino/sheet.dart#L341
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `ceaac22da1a1558eb623d95ba81afd7aa349d9e0` and the full history behind it is present.
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
