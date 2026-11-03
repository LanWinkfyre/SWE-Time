# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Changing WorldEnvironment background setting crashes the editor

<!-- Please search existing issues for potential duplicates before filing yours:
https://github.com/godotengine/godot/issues?q=is%3Aissue
-->

**Godot version:**
<!-- Specify commit hash if using non-official build. -->


**OS/device including version:**
<!-- Specify GPU model, drivers, and the backend (GLES2, GLES3, Vulkan) if graphics-related. -->
OS: Manjaro 20.2.1
GPU: Intel UHD Graphics 620, latest driver
Backend: Vulkan

**Issue description:**
<!-- What happened, and what was expected. -->
On an empty scene and project, adding a sky and then attempting to change its type results in graphical glitches culminating in a crash. I will try to bisect this, will update with details.

**Steps to reproduce:**
1) Create new project and scene
2) Switch to 3D
3) Add WorldEnvironment node
4) Click on environment->New Environment
5) Under `Environment->Background` change mode to `Sky`
A flurry of errors like these show in the console:
```
ERROR: Condition "!sky" is true.
   at: _setup_sky (servers/rendering/renderer_rd/renderer_scene_render_rd.cpp:2301)
ERROR: Condition "!sky" is true.
   at: _setup_sky (servers/rendering/renderer_rd/renderer_scene_render_rd.cpp:2301)
```
5.5) Drag the view around. After 1-2 seconds it starts to slow down and freezes.
6) Change the mode to `Canvas`
7) Move the view. This glitch happens:
![image](https://user-images.githubusercontent.com/30842999/108403026-f0d8dd00-7226-11eb-9d58-d0d15e31a79c.png)

8) After some seconds or after attempting to change mode back to `Sky`, the editor crashes with the stacktrace:
```
DisplayServer::_create_window 8 want rect: 1005, 598, 141, 31 got rect 1005, 598, 141, 31
handle_crash: Program crashed with signal 11
Dumping the backtrace. Please include this when reporting the bug on https://github.com/godotengine/godot/issues
[1] /usr/lib/libc.so.6(+0x3cf80) [0x7f6118556f80] (??:0)
[2] RendererSceneRenderRD::render_scene(RID, Transform const&, CameraMatrix const&, bool, PagedArray<RendererSceneRender::GeometryInstance*> const&, PagedArray<RID> const&, PagedArray<RID> const&, PagedArray<RID> const&, PagedArray<RID> const&, PagedArray<RID> const&, RID, RID, RID, RID, RID, int, float, RendererSceneRender::RenderShadowData const*, int, RendererSceneRender::RenderSDFGIData const*, int, RendererSceneRender::RenderSDFGIUpdateData const*) (/home/lightspot21/repos/godot/servers/rendering/renderer_rd/renderer_scene_render_rd.cpp:7411)
[3] RendererSceneCull::render_empty_scene(RID, RID, RID) (/home/lightspot21/repos/godot/servers/rendering/renderer_scene_cull.cpp:2832 (discriminator 2))
[4] RendererViewport::_draw_viewport(RendererViewport::Viewport*, XRInterface::Eyes) (/home/lightspot21/repos/godot/servers/rendering/renderer_viewport.cpp:416)
[5] RendererViewport::draw_viewports() (/home/lightspot21/repos/godot/servers/rendering/renderer_viewport.cpp:567)
[6] RenderingServerDefault::_draw(bool, double) (/home/lightspot21/repos/godot/servers/rendering/rendering_server_default.cpp:115)
[7] RenderingServerDefault::draw(bool, double) (/home/lightspot21/repos/godot/servers/rendering/rendering_server_default.cpp:388)
[8] Main::iteration() (/home/lightspot21/repos/godot/main/main.cpp:2496)
[9] OS_LinuxBSD::run() (/home/lightspot21/repos/godot/platform/linuxbsd/os_linuxbsd.cpp:261)
[10] /home/lightspot21/repos/godot/bin/godot.linuxbsd.tools.64(main+0x162) [0x1de16f8] (/home/lightspot21/repos/godot/platform/linuxbsd/godot_linuxbsd.cpp:60)
[11] /usr/lib/libc.so.6(__libc_start_main+0xd5) [0x7f6118541b25] (??:0)
[12] /home/lightspot21/repos/godot/bin/godot.linuxbsd.tools.64(_start+0x2e) [0x1de14de] (??:?)
-- END OF BACKTRACE --
```

**Minimal reproduction project:**
<!-- A small Godot project which reproduces the issue. Drag and drop a zip archive to upload it. -->
No need to, it happens in an empty project.

 Visual glitches remain though, maybe I'll open a separate issue
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `5c2fe970b87f8e95306bad0f713567a150b1e442` and the full history behind it is present.
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
