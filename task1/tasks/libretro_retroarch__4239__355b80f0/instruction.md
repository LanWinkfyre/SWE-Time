# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Build/makefile broken on linux with neon enabled.



Building on RPI3 running Raspbian Linux.

```
$./configure --enable-neon
Checking operating system ... Linux 
Checking for suitable working C compiler ... /usr/bin/gcc works
Checking for suitable working C++ compiler ... /usr/bin/g++ works
Checking for pkg-config ... /usr/bin/pkg-config
Checking for availability of switch -std=gnu99 in /usr/bin/gcc ... yes
Checking for availability of switch -Wno-unused-result in /usr/bin/gcc ... yes
Checking for availability of switch -Wno-unused-variable in /usr/bin/gcc ... yes
Checking function bcm_host_init in -lbcm_host ... yes
Checking function sd_get_machine_names in -lsystemd ... no
Checking presence of package egl ... no
Checking existence of -lEGL -lEGL -lGLESv2 -lbcm_host -lvcos -lvchiq_arm ... yes
Checking function ass_library_init in -lass ... no
Checking function pthread_create in -lpthread ... yes
Checking function pthread_key_create in -lpthread ... yes
Checking function dlopen in -ldl ... yes
Checking function socket in -lc ... yes
Checking function getaddrinfo in -lc ... yes
Checking existence of -lminiupnpc ... no
Checking function fcntl in -lc ... yes
Checking function getopt_long in -lc ... yes
Checking presence of package alsa ... 1.0.28
Checking presence of header file sys/soundcard.h ... yes
Checking presence of header file soundcard.h ... no
Checking existence of -lossaudio ... no
Checking function alcOpenDevice in -lopenal ... yes
Checking presence of package rsound >= 1.1 ... no
Checking presence of package libroar ... no
Checking presence of package jack >= 0.120.1 ... 0.124.1
Checking presence of package libpulse ... 5.0
Checking presence of package sdl >= 1.2.10 ... 1.2.15
Checking presence of package sdl2 >= 2.0.0 ... 2.0.4
Notice: SDL drivers will be replaced by SDL2 ones.
Checking presence of package libusb-1.0 >= 1.0.16 ... 1.0.19
Checking presence of header file GL/gl.h ... yes
Checking existence of -lGL ... yes
Checking function cgCreateContext in -lCg ... no
Checking presence of package zlib ... 1.2.8
Checking presence of package libavcodec >= 54 ... 56.1.0
Checking presence of package libavformat >= 54 ... 56.1.0
Checking presence of package libavdevice ... no
Checking presence of package libswresample ... no
Checking presence of package libavresample ... 2.1.0
Checking presence of package libavutil >= 51 ... 54.3.0
Checking presence of package libswscale >= 2.1 ... no
Checking presence of header file libavutil/channel_layout.h ... yes
Notice: FFmpeg built-in support disabled due to missing or unsuitable packages.
Checking function dlopen in -ldl ... yes
Checking presence of package gbm >= 9.0 ... no
Checking presence of package libdrm ... 2.4.71
Checking presence of package libxml-2.0 ... no
Checking presence of package glesv2 ... no
Checking existence of -lGLESv2 -lEGL -lGLESv2 -lbcm_host -lvcos -lvchiq_arm ... yes
Checking presence of package vg ... no
Checking existence of -lOpenVG -lEGL -lGLESv2 -lbcm_host -lvcos -lvchiq_arm ... yes
Checking presence of package libv4l2 ... no
Checking presence of package freetype2 ... 18.0.12
Checking presence of package x11 ... 1.6.2
Checking presence of package xcb ... 1.10
Checking presence of package wayland-egl ... no
Checking presence of package xkbcommon >= 0.3.2 ... 0.4.3
Checking presence of package dbus-1 ... 1.8.20
Checking presence of package xext ... 1.3.3
Checking presence of package xxf86vm ... 1.1.3
Checking presence of package xinerama ... no
Checking presence of package xv ... no
Checking presence of package libudev ... 215
Checking presence of header file linux/parport.h ... yes
Checking presence of header file linux/ppdev.h ... yes
Checking function strlcpy in -lc ... no
Checking function strcasestr in -lc ... yes
Checking function mmap in -lc ... yes
Checking function vkCreateInstance in -lvulkan ... no
Checking presence of predefined macro __ARM_NEON__ ... yes
Creating make config: config.mk
Creating config header: config.h

$ make
CC input/drivers/linuxraw_input.c
CC input/common/linux_common.c
CC input/common/epoll_common.c
CC input/drivers_joypad/linuxraw_joypad.c
CC frontend/drivers/platform_linux.c
CC version_git.c
CC frontend/frontend.c
CC frontend/frontend_driver.c
CC frontend/drivers/platform_null.c
CC ui/ui_companion_driver.c
CC ui/drivers/ui_null.c
CC ui/drivers/null/ui_null_window.c
CC ui/drivers/null/ui_null_browser_window.c
CC ui/drivers/null/ui_null_msg_window.c
CC ui/drivers/null/ui_null_application.c
CC core_impl.c
CC retroarch.c
CC dirs.c
CC paths.c
CC input/input_keyboard.c
CC command.c
CC msg_hash.c
CC intl/msg_hash_us.c
CC runloop.c
CC libretro-common/algorithms/mismatch.c
CC libretro-common/queues/task_queue.c
CC tasks/task_content.c
CC tasks/task_save.c
CC tasks/task_file_transfer.c
CC tasks/task_image.c
CC libretro-common/encodings/encoding_utf.c
CC libretro-common/encodings/encoding_crc32.c
CC libretro-common/lists/file_list.c
CC libretro-common/lists/dir_list.c
CC libretro-common/file/retro_dirent.c
CC libretro-common/streams/file_stream.c
CC libretro-common/streams/interface_stream.c
CC libretro-common/streams/memory_stream.c
CC libretro-common/file/retro_stat.c
CC libretro-common/lists/string_list.c
CC libretro-common/string/stdstring.c
CC libretro-common/memmap/memalign.c
CC setting_list.c
CC list_special.c
CC libretro-common/file/nbio/nbio_stdio.c
CC libretro-common/file/file_path.c
CC file_path_special.c
CC file_path_str.c
CC libretro-common/hash/rhash.c
CC audio/audio_driver.c
CC input/input_driver.c
CC gfx/video_coord_array.c
CC gfx/video_driver.c
CC camera/camera_driver.c
CC wifi/wifi_driver.c
CC location/location_driver.c
CC driver.c
CC configuration.c
CC libretro-common/dynamic/dylib.c
CC dynamic.c
CC cores/dynamic_dummy.c
CC libretro-common/queues/message_queue.c
CC managers/state_manager.c
CC gfx/drivers_font_renderer/bitmapfont.c
CC tasks/task_autodetect.c
CC input/input_autodetect_builtin.c
CC input/input_joypad_driver.c
CC input/input_config.c
CC input/input_keymaps.c
CC input/input_remapping.c
CC tasks/task_overlay.c
CC input/input_overlay.c
CC patch.c
CC libretro-common/queues/fifo_queue.c
CC managers/core_option_manager.c
CC libretro-common/compat/compat_fnmatch.c
CC libretro-common/compat/compat_posix_string.c
CC managers/cheat_manager.c
CC core_info.c
CC libretro-common/file/config_file.c
CC libretro-common/file/config_file_userdata.c
CC tasks/task_screenshot.c
CC libretro-common/gfx/scaler/scaler.c
CC gfx/drivers_shader/shader_null.c
CC gfx/video_shader_driver.c
CC gfx/video_shader_parse.c
CC libretro-common/gfx/scaler/pixconv.c
CC libretro-common/gfx/scaler/scaler_int.c
CC libretro-common/gfx/scaler/scaler_filter.c
CC gfx/font_driver.c
CC gfx/video_filter.c
CC libretro-common/audio/resampler/audio_resampler.c
CC audio/audio_dsp_filter.c
CC libretro-common/audio/resampler/drivers/sinc_resampler.c
CC libretro-common/audio/resampler/drivers/nearest_resampler.c
CC libretro-common/audio/resampler/drivers/null_resampler.c
CC location/drivers/nulllocation.c
CC camera/drivers/nullcamera.c
CC wifi/drivers/nullwifi.c
CC gfx/drivers/nullgfx.c
CC audio/drivers/nullaudio.c
CC input/drivers/nullinput.c
CC input/drivers_hid/null_hid.c
CC input/drivers_joypad/null_joypad.c
CC playlist.c
CC movie.c
CC record/record_driver.c
CC record/drivers/record_null.c
CC libretro-common/features/features_cpu.c
CC performance_counters.c
CC verbosity.c
CC audio/drivers_resampler/cc_resampler.c
CC intl/msg_hash_de.c
CC intl/msg_hash_eo.c
CC intl/msg_hash_es.c
CC intl/msg_hash_fr.c
CC intl/msg_hash_it.c
CC intl/msg_hash_ja.c
CC intl/msg_hash_nl.c
CC intl/msg_hash_pl.c
CC intl/msg_hash_pt.c
CC intl/msg_hash_ru.c
CC intl/msg_hash_vn.c
CC intl/msg_hash_chs.c
CC libretro-common/compat/compat_strl.c
CC libretro-common/formats/image_texture.c
CC cores/libretro-imageviewer/image_core.c
CC libretro-db/bintree.c
CC libretro-db/libretrodb.c
CC libretro-db/query.c
CC libretro-db/rmsgpack.c
CC libretro-db/rmsgpack_dom.c
CC database_info.c
CC tasks/task_database.c
CC tasks/task_database_cue.c
CC audio/drivers/oss.c
CC audio/drivers/alsa.c
CC audio/drivers/alsathread.c
CC audio/drivers/openal.c
CC audio/drivers/jack.c
CC audio/drivers/pulse.c
make: *** No rule to make target 'obj-unix/audio/drivers_resampler/sinc_resampler_neon.o', needed by 'retroarch'.  Stop.
```
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `93b29aab5ad5677202dac8004fa9b9f60034fc73` and the full history behind it is present.
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
