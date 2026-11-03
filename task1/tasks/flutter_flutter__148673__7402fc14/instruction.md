# Locate the commit that introduced this regression

A regression was reported against `flutter/flutter`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Keyboard disappears in landscape orientation (phone) on the next TextField focus (Broken since Flutter v3.22.0)

### Steps to reproduce
- Use a phone in landscape orientation (I use pixel 3a, simulator)
- Focus the first TextField
- Go to the next TextField with keyboard or click on the next TextField.
- Keyboard disappears, while in flutter 3.19.2 or before it worked fine.


### Expected results

It is expected that the keyboard also stays visible if the focus goes to the next TextField when the phone is in in landscape orientation.
- Flutter 3.22.0: Keyboard disappears
- Flutter 3.19.2 Keyboard stays visible like expected (like the versions before)

### Actual results
- In landscape orientation the keyboard disappears when the next TextField gets focus.
- You need to click the TextField again to show the keyboard.

### Code sample

<details open><summary>Code sample</summary>

```dart
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(widget.title),
        ),
        body: CustomScrollView(slivers: [
          SliverToBoxAdapter(
              child: Container(
            height: 500,
            color: Colors.amber,
          )),
          SliverToBoxAdapter(child: Builder(builder: (context) {
            return const Column(
              children: [
                SizedBox(
                  height: 72.0,
                  child: Row(children: [
                    Expanded(
                        child:
                            TextField(textInputAction: TextInputAction.next)),
                    SizedBox(
                      width: 8.0,
                    ),
                    Expanded(child: TextField()),
                  ]),
                ),
              ],
            );
          })),
          SliverToBoxAdapter(
              child: Container(
            height: 500,
            color: Colors.amber,
          )),
        ]));
  }
}
```

</details>


### Screenshots or Video

Difference flutter 3.19.2 vs 3.22.0
<details open>
<summary>Flutter 3.22.0, No Keyboard</summary>


![image](https://github.com/flutter/flutter/assets/32017307/cc0d2a79-d4a5-4b3e-a7b3-2417e6dd2284)



</details>




### Logs

<details open><summary>Logs</summary>

```console
No log at moment.
```

</details>


### Flutter Doctor output

<details open><summary>Doctor output Flutter 3.22.0</summary>

```console
Doctor summary (to see all details, run flutter doctor -v):
[√] Flutter (Channel stable, 3.22.0, on Microsoft Windows [Version
    10.0.22631.3593], locale en-NL)
[√] Windows Version (Installed version of Windows is version 10 or higher)
[!] Android toolchain - develop for Android devices (Android SDK version 34.0.0)
    X cmdline-tools component is missing
      Run `path/to/sdkmanager --install "cmdline-tools;latest"`
      See https://developer.android.com/studio/command-line for more details.
    X Android license status unknown.
      Run `flutter doctor --android-licenses` to accept the SDK licenses.
      See https://flutter.dev/docs/get-started/install/windows#android-setup for
      more details.
[√] Chrome - develop for the web
[X] Visual Studio - develop Windows apps
    X Visual Studio not installed; this is necessary to develop Windows apps.
      Download at https://visualstudio.microsoft.com/downloads/.
      Please install the "Desktop development with C++" workload, including all of
      its default components
[√] Android Studio (version 2023.3)
[√] VS Code (version 1.89.1)
[√] Connected device (5 available)
[√] Network resources
```

</details>

<details open><summary>Doctor output Flutter 3.19.2</summary>

```console
Success
PS C:\Repositories\flutter\test\keyboard_bug> flutter doctor   
Doctor summary (to see all details, run flutter doctor -v):
[√] Flutter (Channel stable, 3.19.2, on Microsoft Windows [Version
    10.0.22631.3593], locale en-NL)
[√] Windows Version (Installed version of Windows is version 10 or higher)
[!] Android toolchain - develop for Android devices (Android SDK version 34.0.0)
    X cmdline-tools component is missing
      Run `path/to/sdkmanager --install "cmdline-tools;latest"`
      See https://developer.android.com/studio/command-line for more details.      
    X Android license status unknown.
      Run `flutter doctor --android-licenses` to accept the SDK licenses.
      See https://flutter.dev/docs/get-started/install/windows#android-setup for   
      more details.
[√] Chrome - develop for the web
[X] Visual Studio - develop Windows apps
    X Visual Studio not installed; this is necessary to develop Windows apps.      
      Download at https://visualstudio.microsoft.com/downloads/.
      Please install the "Desktop development with C++" workload, including all of 
      its default components
[√] Android Studio (version 2023.3)
[√] VS Code (version 1.89.1)
[√] Connected device (5 available)
[√] Network resources
```

</details>

  

<details>
<summary>git bisect (tailed output)</summary>


</details>
```

## What you have

- `/testbed/repo` is a git clone of `flutter/flutter` truncated just after the regression was
  reported.  `HEAD` is `6067d8f2195d303fca946ae5400c05cc82f2e2e7` and the full history behind it is present.
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
