# Locate the commit that introduced this regression

A regression was reported against `godotengine/godot`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Project crashes at launch on master

### Tested versions


Works fine in 4.7 stable.

### System information

Godot v4.7.stable - Windows 10 (build 19045) - Multi-window, 2 monitors - Vulkan (Forward+) - dedicated NVIDIA GeForce GTX 1060 (NVIDIA; 32.0.15.8228) - Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz (8 threads) - 15.95 GiB memory - WASAPI (44100 Hz, Stereo/mono)

### Issue description

I came upon some random MRP that crashes for me. The crash happens on DEV_ASSERT:
```
RenderingDeviceGraph::end(bool p_reorder_commands, bool p_full_barriers, RenderingDeviceDriver::CommandBufferID & r_command_buffer, RenderingDeviceGraph::CommandBufferPool & r_command_buffer_pool) Line 2605 (c:\godot_source\servers\rendering\rendering_device_graph.cpp:2605)
RenderingDevice::_end_frame() Line 8112 (c:\godot_source\servers\rendering\rendering_device.cpp:8112)
RenderingDevice::swap_buffers(bool p_present) Line 7870 (c:\godot_source\servers\rendering\rendering_device.cpp:7870)
RendererCompositorRD::end_frame(bool p_present) Line 136 (c:\godot_source\servers\rendering\renderer_rd\renderer_compositor_rd.cpp:136)
RenderingServerDefault::_draw(bool p_swap_buffers, double frame_step) Line 115 (c:\godot_source\servers\rendering\rendering_server_default.cpp:115)
RenderingServerDefault::draw(bool p_present, double frame_step) Line 451 (c:\godot_source\servers\rendering\rendering_server_default.cpp:451)
Main::iteration() Line 5086 (c:\godot_source\main\main.cpp:5086)
ProgressDialog::_update_ui() Line 152 (c:\godot_source\editor\gui\progress_dialog.cpp:152)
ProgressDialog::task_step(const String & p_task, const String & p_state, int p_step, bool p_force_redraw) Line 250 (c:\godot_source\editor\gui\progress_dialog.cpp:250)
EditorNode::progress_task_step(const String & p_task, const String & p_state, int p_step, bool p_force_refresh) Line 5963 (c:\godot_source\editor\editor_node.cpp:5963)
EditorProgress::step(const String & p_state, int p_step, bool p_force_refresh) Line 224 (c:\godot_source\editor\editor_node.cpp:224)
EditorFileSystem::_first_scan_filesystem() Line 323 (c:\godot_source\editor\file_system\editor_file_system.cpp:323)
EditorFileSystem::scan() Line 1098 (c:\godot_source\editor\file_system\editor_file_system.cpp:1098)
EditorNode::_notification(int p_what) Line 917 (c:\godot_source\editor\editor_node.cpp:917)
EditorNode::_notification_forwardv(int p_notification) Line 121 (c:\godot_source\editor\editor_node.h:121)
Object::_notification_forward(int p_notification) Line 910 (c:\godot_source\core\object\object.cpp:910)
Object::notification(int p_notification, bool p_reversed) Line 725 (c:\godot_source\core\object\object.h:725)
SceneTree::_process_group(SceneTree::ProcessGroup * p_group, bool p_physics) Line 1230 (c:\godot_source\scene\main\scene_tree.cpp:1230)
SceneTree::_process(bool p_physics) Line 1307 (c:\godot_source\scene\main\scene_tree.cpp:1307)
SceneTree::process(double p_time) Line 721 (c:\godot_source\scene\main\scene_tree.cpp:721)
```
However if I remove it, it crashes in a different place:
```
[0] 7ff77e545ae9 (main+245ae9) - LocalVector<int,unsigned int,0,0>::operator[] (C:\godot_source\core\templates\local_vector.h:206)
[1] 7ff78385d275 (main+555d275) - RenderingDeviceGraph::end (C:\godot_source\servers\rendering\rendering_device_graph.cpp:2672)
[2] 7ff7838bcb55 (main+55bcb55) - RenderingDevice::_end_frame (C:\godot_source\servers\rendering\rendering_device.cpp:8112)
[3] 7ff7838c3fd9 (main+55c3fd9) - RenderingDevice::swap_buffers (C:\godot_source\servers\rendering\rendering_device.cpp:7870)
[4] 7ff783db51f6 (main+5ab51f6) - RendererCompositorRD::end_frame (C:\godot_source\servers\rendering\renderer_rd\renderer_compositor_rd.cpp:136)
[5] 7ff78382d528 (main+552d528) - RenderingServerDefault::_draw (C:\godot_source\servers\rendering\rendering_server_default.cpp:115)
[6] 7ff78382eae6 (main+552eae6) - RenderingServerDefault::draw (C:\godot_source\servers\rendering\rendering_server_default.cpp:451)
[7] 7ff77e408072 (main+108072) - Main::iteration (C:\godot_source\main\main.cpp:5086)
[8] 7ff780a9544c (main+279544c) - ProgressDialog::_update_ui (C:\godot_source\editor\gui\progress_dialog.cpp:152)
[9] 7ff780a95fef (main+2795fef) - ProgressDialog::task_step (C:\godot_source\editor\gui\progress_dialog.cpp:250)
[10] 7ff7809019b9 (main+26019b9) - EditorNode::progress_task_step (C:\godot_source\editor\editor_node.cpp:5963)
[11] 7ff7808d4f2e (main+25d4f2e) - EditorProgress::step (C:\godot_source\editor\editor_node.cpp:224)
[12] 7ff7809fae32 (main+26fae32) - EditorFileSystem::_first_scan_filesystem (C:\godot_source\editor\file_system\editor_file_system.cpp:323)
[13] 7ff780a1111e (main+271111e) - EditorFileSystem::scan (C:\godot_source\editor\file_system\editor_file_system.cpp:1098)
[14] 7ff7808fd5b7 (main+25fd5b7) - EditorNode::_notification (C:\godot_source\editor\editor_node.cpp:917)
[15] 7ff7809ab04d (main+26ab04d) - EditorNode::_notification_forwardv (C:\godot_source\editor\editor_node.h:121)
[16] 7ff78486892b (main+656892b) - Object::_notification_forward (C:\godot_source\core\object\object.cpp:910)
[17] 7ff77e3a7f6a (main+a7f6a) - Object::notification (C:\godot_source\core\object\object.h:725)
[18] 7ff7820d03c4 (main+3dd03c4) - SceneTree::_process_group (C:\godot_source\scene\main\scene_tree.cpp:1230)
[19] 7ff7820d0ae0 (main+3dd0ae0) - SceneTree::_process (C:\godot_source\scene\main\scene_tree.cpp:1307)
[20] 7ff7820d64be (main+3dd64be) - SceneTree::process (C:\godot_source\scene\main\scene_tree.cpp:721)
[21] 7ff77e407e2e (main+107e2e) - Main::iteration (C:\godot_source\main\main.cpp:5058)
[22] 7ff77e344bb6 (main+44bb6) - OS_Windows::run (C:\godot_source\platform\windows\os_windows.cpp:2362)
[23] 7ff77e3c4879 (main+c4879) - widechar_main (C:\godot_source\platform\windows\godot_windows.cpp:98)
[24] 7ff77e3c4973 (main+c4973) - _main (C:\godot_source\platform\windows\godot_windows.cpp:125)
[25] 7ff77e3c49b2 (main+c49b2) - main (C:\godot_source\platform\windows\godot_windows.cpp:139)
[26] 7ff77e3c458d (main+c458d) - WinMain (C:\godot_source\platform\windows\godot_windows.cpp:153)
[27] 7ff785383906 (main+7083906) - __scrt_common_main_seh (D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288)
[28] 7ff77e336d0a (main+36d0a) - ShimMainCRTStartup (C:\godot_source\platform\windows\cpu_feature_validation.c:74)
[29] 7ff9bbbe7374 (kernel32.dll+17374) - <couldn't map PC to fn name>
```

### Steps to reproduce

Open the MRP.

### Minimal reproduction project (MRP)

[reproduce-animation-bug.zip](https://github.com/user-attachments/files/29176136/reproduce-animation-bug.zip)





```
ERROR: Command can't have itself as a dependency.
   at: _add_command_to_graph (servers/rendering/rendering_device_graph.cpp:623)
ERROR: FATAL: DEV_ASSERT failed  "(command_list_node.command_index != int32_t(i)) && "Command can't have itself as a dependency."" is false.
   at: end (servers/rendering/rendering_device_graph.cpp:2605)
```
```

## What you have

- `/testbed/repo` is a git clone of `godotengine/godot` truncated just after the regression was
  reported.  `HEAD` is `f964fa714f503bd063b96f6194eb3e45355c1084` and the full history behind it is present.
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
