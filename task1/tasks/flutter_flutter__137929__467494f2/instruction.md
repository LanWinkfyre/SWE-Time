# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
RouteSettings encoded name is automatically decoded in Flutter 3.13

### Is there an existing issue for this?

- [X] I have searched the [existing issues](https://github.com/flutter/flutter/issues)
- [X] I have read the [guide to filing a bug](https://flutter.dev/docs/resources/bug-reports)

### Steps to reproduce

1. Run the above sample as web app with Flutter 3.7
2. Click on the "Navigate" button.
3. Observe the url in the browser. It will be like `http://localhost:53060/#/test?q=Hello%21`
4. Now Run the same sample with Flutter 3.13
5. Click on the "Navigate" button.
6. Observe the url in the browser. It will be like `http://localhost:53060/#/test?q=Hello!`
7. Note the difference in steps 3 and 7. Exclamation sign (!) is kept encoded in Flutter 3.7 but not in Flutter 3.13

### Expected results

Using Flutter 3.13, it should remain like `http://localhost:53060/#/test?q=Hello%21` as in Flutter 3.7

### Actual results

Exclamation sign is not encoded in Flutter 3.13

### Code sample

<details><summary>Code sample</summary>

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatefulWidget {
  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  @override
  void initState() {
    super.initState();
  }

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: Scaffold(
        backgroundColor: Colors.transparent,
        body: Builder(
          builder: (context) {
            return Center(
              child: TextButton(
                  onPressed: () {
                    String name = "/test";
                    // append the query parameter
                    name += "?q=${Uri.encodeQueryComponent("Hello!")}";

                    Navigator.of(context).push(MaterialPageRoute(
                      settings: RouteSettings(name: name),
                      builder: (context) {
                        return Scaffold(
                          body: Container(
                            child: Center(
                              child: Text("Another route"),
                            ),
                          ),
                        );
                      },
                    ));
                  },
                  child: Text("Navigate")),
            );
          }
        ),
      ),
    );
  }
}

```

</details>


### Screenshots or Video

<details>
<summary>Screenshots / Video demonstration</summary>



</details>


### Logs

<details><summary>Logs</summary>

```console
[Paste your logs here]
```

</details>


### Flutter Doctor output

<details><summary>Doctor output</summary>



</details>


Thanks for the report! Reproduced this issue on the latest Flutter stable and master channels. The issue didn't occur on the previous stable release `3.10.6`.

<details>
<summary>flutter doctor -v (stable and master)</summary>




</details>


 cc: @chunhtai for thoughts.
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `12de94d152ad14c0cdf2aa615f5050fdd6be3329` and the full history behind it is present.
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
