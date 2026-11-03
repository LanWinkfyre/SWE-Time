# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Keyboard flickers/dismisses momentarily when switching focus between TextFields on iOS

### Steps to reproduce

1. Run the code sample below on a physical iOS device.
2. Tap on the first TextField to focus it and bring up the software keyboard.
3. Tap on the second TextField to move focus.
4. Repeat switching focus between the two fields.

### Expected results

The keyboard should remain static and not slide / flicker when switching focus between TextFields.

<img src="https://github.com/user-attachments/assets/1978058a-af34-4148-a9c8-66016d0bb13f" width="300" />

### Actual results

The keyboard briefly dismisses and reappears (flickers) each time focus moves from one TextField to another. It appears the framework is unfocusing the current field before focusing the next one, causing the keyboard to momentarily hide and re-show. This creates a jarring visual experience and causes the layout to shift briefly.

<img src="https://github.com/user-attachments/assets/59cd3b9b-e2e1-494e-a2b9-03761ac54baf" width="300" />

### Code sample

<details open><summary>Code sample</summary>

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(colorScheme: .fromSeed(seedColor: Colors.deepPurple)),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            spacing: 8,
            mainAxisAlignment: .center,
            children: [
              TextField(
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'field 1',
                ),
              ),
              TextField(
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'field 2',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

```

</details>

### Flutter Doctor output

<details open><summary>Doctor output</summary>



</details>


We saw the same symptom in Zulip: https://github.com/zulip/zulip-flutter/issues/1974
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `640a089bb4ec8d10d469d19bec17ca1614dc093a` and the full history behind it is present.
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
