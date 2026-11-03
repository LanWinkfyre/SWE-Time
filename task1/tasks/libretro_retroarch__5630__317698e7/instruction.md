# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Segfault in the quick menu

## Description

I get this segfault:

```
Thread 1 "retroarch" received signal SIGSEGV, Segmentation fault.
menu_event_kb_set (down=false, key=3976642272) at menu/menu_event.c:118
118	      menu_event_kb_set_internal(key, ((menu_event_kb_is_set(key) & 1) << 1) | down);
(gdb) bt
#0  menu_event_kb_set (down=false, key=3976642272) at menu/menu_event.c:118
#1  0x00005555555dd334 in input_keyboard_event (down=<optimized out>, code=3976642272, character=0, mod=<optimized out>, device=<optimized out>) at input/input_driver.c:2069
#2  0x00007fffeddad1c8 in ffi_call_unix64 () from /usr/lib/libffi.so.6
#3  0x00007fffeddacc2a in ffi_call () from /usr/lib/libffi.so.6
#4  0x00007ffff6684bad in ?? () from /usr/lib/libwayland-client.so.0
#5  0x00007ffff6681679 in ?? () from /usr/lib/libwayland-client.so.0
#6  0x00007ffff66829b4 in wl_display_dispatch_queue_pending () from /usr/lib/libwayland-client.so.0
#7  0x00005555556dee7e in flush_wayland_fd (data=<optimized out>) at gfx/drivers_context/wayland_ctx.c:609
#8  gfx_ctx_wl_check_window (data=0x5555571d3700, quit=0x7fffffffe306, resize=0x7fffffffe307, width=0x7fffffffe308, height=0x7fffffffe30c, is_shutdown=<optimized out>)
    at gfx/drivers_context/wayland_ctx.c:637
#9  0x00005555555e37b9 in video_context_driver_check_window (size_data=size_data@entry=0x7fffffffe310) at gfx/video_driver.c:2843
#10 0x00005555556edcbd in gl_alive (data=0x555557284fe0) at gfx/drivers/gl.c:2234
#11 0x00005555555e33fb in video_driver_get_status (frame_count=frame_count@entry=0x7fffffffe3a8, is_alive=is_alive@entry=0x7fffffffe3a7, is_focused=is_focused@entry=0x7fffffffe3a6)
    at gfx/video_driver.c:2657
#12 0x000055555559c938 in runloop_check_state (settings=settings@entry=0x7ffff7fc8010, input_nonblock_state=input_nonblock_state@entry=false, sleep_ms=0x7fffffffe52c) at retroarch.c:2410
#13 0x00005555555a0c24 in runloop_iterate (sleep_ms=0x7fffffffe52c) at retroarch.c:3056
#14 0x000055555559a6f0 in rarch_main (argc=<optimized out>, argv=<optimized out>, data=0x0) at frontend/frontend.c:131
#15 0x00007fffef473f6a in __libc_start_main () from /usr/lib/libc.so.6
#16 0x000055555559780a in _start ()
```

### Steps to reproduce the bug

1. Launch a game from a Playlist
2. Trigger the quick menu
3. Hit DOWN quickly

### Bisect Results

[Try to bisect and tell us when this started happening]

### Version/Commit
You can find this information under Information/System Information

- RetroArch: [version/commit]

### Environment information

- OS: Arch Linux with Wayland
- Compiler: [In case you are running local builds]
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `d1278306c75495352e50129fd9b09bcf2b883368` and the full history behind it is present.
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
