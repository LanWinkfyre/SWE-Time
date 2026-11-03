# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
It's impossible to run the project from the editor.

**Operating system or device - Godot version:**


**Issue description:**
After clicking 'play' button nothing changes in the editor. Only output/debug panel gets unfolded. 
![play project](https://user-images.githubusercontent.com/6129594/28887203-98fb19f8-77bc-11e7-9e00-f60e68ecba52.gif)


Console output:
```
Usage: /home/kubeczek/git/Godot/MyFork/godot/bin/godot.x11.tools.64 [options] [path to scene or 'project.godot' file]
Options:
  -h, --help                       Display this help message.
  --path <directory>               Path to the project (<directory> must contain a 'project.godot' file).
  -e, --editor                     Bring up the editor instead of running the scene.
  --test <test>                    Run a test ('string', 'containers', 'math', 'render', 'multimesh', 'gui', 'io', 'shaderlang', 'physics').
  -r, --resolution <W>x<H>         Request window resolution.
  -p, --position <X>,<Y>           Request window position.
  -f, --fullscreen                 Request fullscreen mode.
  -m, --maximized                  Request a maximized window.
  -w, --windowed                   Request windowed mode.
  --video-driver <driver>          Video driver ('GLES3').
  --low-dpi                        Force low-DPI mode (macOS only).
  --audio-driver <driver>          Audio driver ('PulseAudio', 'ALSA').
  --render-thread <mode>           Render thread mode ('unsafe', 'safe', 'separate').
  -s, --script <script>            Run a script.
  -d, --debug                      Debug (local stdout debugger).
  -r, --remote-debug <address>     Remote debug (<ip>:<port> host address).
  --frame-delay <ms>               Simulate high CPU load (delay each frame by <ms> milliseconds).
  --time-scale <scale>             Force time scale (higher values are faster, 1.0 is normal speed).
  -b, --breakpoints                Breakpoint list as source::line comma-separated pairs, no spaces (use %20, %2C, ... instead).
  -v, --verbose                    Use verbose stdout mode.
  -l, --language <locale>          Use a specific locale (<locale> being a two-letter code).
  --remote-fs <host/IP>[:<port>]   Remote filesystem.
  --remote-fs-password <password>  Password for remote filesystem.
  --doctool <file>                 Dump the whole engine API to <file> in XML format. If <file> exists, it will be merged.
  --no-docbase                     Disallow dumping the base types (used with --doctool).
  --export <target>                Export the project using the given export target.
WARNING: not found: editor_plugins/enabled
WARNING: not found: editor_plugins/enabled
running: /home/kubeczek/git/Godot/MyFork/godot/bin/godot.x11.tools.64 --path /home/kubeczek/projects/wip/Converting/issues/td3_physic_issue/RigidBodyInKinematic --remote-debug 127.0.0.1:6007 --editor-pid 30573 -p 0x0 res://gameplay/Level/Levels/TestLevel2/TestLevel2.tscn
Invalid position argument: 0x0

```

**Steps to reproduce:**
1. Download sample project
2. Open it
3. Click run button.

**Link to minimal example project:**
[RigidBodyInKinematic.zip](https://github.com/godotengine/godot/files/1194798/RigidBodyInKinematic.zip)




@Calinou can you check?
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `0586524b9ce67bdcab5cef88397c44bb7b9e46fb` and the full history behind it is present.
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
