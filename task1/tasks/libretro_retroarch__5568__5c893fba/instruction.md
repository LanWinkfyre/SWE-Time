# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
RetroArch crashes if video_driver is set to an incorrect value.

## Description

If the `video_driver` config setting is incorrectly set in `~/.config/retroarch/retroarch.cfg` to something like `video_driver = "opengl"` instead of the correct `video_driver = "gl"` RetroArch will segfault.  Interestingly this only occurs if `deps/SPIRV-Cross` is present and can be avoided with `./configure --disable-vulkan`.

### Expected behavior

RetroArch should ignore the incorrect setting and fall back to a safe default. A warning could also be printed in the log.

### Actual behavior

RetroArch will segfault.
```
Thread 1 "retroarch" received signal SIGSEGV, Segmentation fault.
0x0000000000000000 in ?? ()
(gdb) bt
#0  0x0000000000000000 in ?? ()
#1  0x00000000005b76c7 in vulkan_context_init (vk=0x163dcc0, type=VULKAN_WSI_XCB)
    at gfx/common/vulkan_common.c:1764
#2  0x00000000005877c1 in gfx_ctx_x_init (video_info=0x7fffffffd930,
    data=0x163be20) at gfx/drivers_context/x_ctx.c:509
#3  0x000000000045becb in video_context_driver_init (data=0x163be20,
    ctx=0xcafde0 <gfx_ctx_x>, ident=0x7fb048ac2ad9 "", api=GFX_CTX_VULKAN_API,
    major=1, minor=0, hw_render_ctx=false) at gfx/video_driver.c:2744
#4  0x000000000045c04f in video_context_driver_find_driver (data=0x163be20,
    ident=0x7fb048ac2ad9 "", api=GFX_CTX_VULKAN_API, major=1, minor=0,
    hw_render_ctx=false) at gfx/video_driver.c:2795
#5  0x000000000045c0d0 in video_context_driver_init_first (data=0x163be20,
    ident=0x7fb048ac2ad9 "", api=GFX_CTX_VULKAN_API, major=1, minor=0,
    hw_render_ctx=false) at gfx/video_driver.c:2824
#6  0x00000000005abdbf in vulkan_get_context (vk=0x163be20)
    at gfx/drivers/vulkan.c:69
#7  0x00000000005aeb92 in vulkan_init (video=0x7fffffffdbe0,
    input=0xcfa300 <current_input>, input_data=0xcfa308 <current_input_data>)
    at gfx/drivers/vulkan.c:1106
#8  0x0000000000458df5 in video_driver_init_internal (
    video_is_threaded=0x7fffffffdca7) at gfx/video_driver.c:1038
#9  0x000000000045a1df in video_driver_init (video_is_threaded=0x7fffffffdca7)
    at gfx/video_driver.c:1733
#10 0x000000000045e862 in drivers_init (flags=255) at driver.c:351
#11 0x00000000004188e0 in retroarch_main_init (argc=1, argv=0x7fffffffe278)
    at retroarch.c:1294
#12 0x000000000042ee8a in content_load (info=0x7fffffffe140)
    at tasks/task_content.c:276
#13 0x000000000042ffd8 in task_load_content (content_info=0x7fffffffe140,
    content_ctx=0x7fffffffe060, launched_from_menu=true, launched_from_cli=true,
    error_string=0x7fffffffe058) at tasks/task_content.c:862
#14 0x00000000004313c1 in task_load_content_callback (
    content_info=0x7fffffffe140, loading_from_menu=true, loading_from_cli=true)
    at tasks/task_content.c:1533
#15 0x0000000000431531 in task_push_load_content_from_cli (core_path=0x0,
    fullpath=0x0, content_info=0x7fffffffe140, type=CORE_TYPE_PLAIN, cb=0x0,
    user_data=0x0) at tasks/task_content.c:1597
#16 0x0000000000414da3 in rarch_main (argc=1, argv=0x7fffffffe278, data=0x0)
    at frontend/frontend.c:115
#17 0x0000000000414e26 in main (argc=1, argv=0x7fffffffe278)
    at frontend/frontend.c:151
```
Full GDB log. - https://pastebin.com/K4ZfRQkH

### Steps to reproduce the bug

1. Change `video_driver` in `~/.config/retroarch/retroarch.cfg` to `video_driver = "foo"`.
2. Start RetroArch.
3. It crashes.

### Bisect Results





### Version/Commit
You can find this information under Information/System Information



### Environment information

- OS: `Slackware64-current`
- Compiler: `gcc-7.2.0`
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `b0f8a570b5434e798d1cddccb4c9bb2621f62c73` and the full history behind it is present.
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
