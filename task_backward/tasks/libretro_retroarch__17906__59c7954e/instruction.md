# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Retroarch no longer builds on linux

### Is there an existing issue for this?

- [x] This is a bug in RetroArch frontend
- [x] I have searched the existing issues

### Description

Retroarch no longer builds.  During ./configure the following is thrown:
```
Checking presence of package wayland-scanner >= 1.12 ... 1.22.0
Could not open input file: No such file or directory
Error: Failed generating wayland protocols.
```
Presumably the failure is related to `libdecor` as it is the next package to be checked.

Here is the information from the bisect (@Sunderland93 can you help?)


### Expected behavior

RetroArch builds

### Steps to reproduce the bug

1. $ git clone --recursive https://github.com/libretro/RetroArch.git
2. $ cd RetroArch
3. $ ./fetch-submodules.sh
4. $ ./configure

### Version/Commit



### Bisect Results



### Present in the nightly version

I don't know

### Platform & operating system

Linux Mint 22.1 / kernel 6.11

### Affected Cores

_No response_

### Environment information

gcc 14.2.0

### Relevant log output

```shell
$ ./configure
Checking operating system ... Linux (Linux Mint 22.1 Xia 22.1)
Checking for suitable working C compiler ... /usr/bin/gcc works
Checking for suitable working C++ compiler ... /usr/bin/g++ works
Checking for pkg-config ... /usr/bin/pkgconf
Checking for availability of switch -std=gnu99 in /usr/bin/gcc ... yes
Checking for availability of switch -std=c++11 in /usr/bin/g++ ... yes
Checking for availability of switch -std=c++17 in /usr/bin/g++ ... yes
Checking for availability of switch -Wno-unused-result in /usr/bin/gcc ... yes
Checking for availability of switch -Wno-unused-variable in /usr/bin/gcc ... yes
Checking function sd_get_machine_names in -lsystemd ... yes
Checking presence of package bcm_host ... no
Checking function bcm_host_init in -lbcm_host ... no
Checking presence of header file EGL/eglext.h ... yes
Checking presence of package egl ... 1.5
Checking presence of header file lzma.h ... yes
Checking function ass_library_init in -lfribidi -lass ... no
Checking function pthread_create in -lpthread ... yes
Checking function pthread_key_create in -lpthread ... yes
Checking presence of package check >= 0.15 ... no
Checking presence of header file scsi/sg.h ... yes
Checking function dlopen in -ldl ... yes
Checking function socket in -lc ... yes
Checking function getaddrinfo in -lc ... yes
Checking function fcntl in -lc ... yes
Checking function getopt_long in -lc ... yes
Checking presence of package alsa ... 1.2.11
Checking presence of package libsixel >= 1.6.0 ... no
Checking presence of predefined macro AUDIO_SETINFO in sys/audioio.h ... no
Checking presence of header file sys/soundcard.h ... yes
Checking presence of header file soundcard.h ... no
Checking existence of -lossaudio ... no
Checking presence of package rsound >= 1.1 ... no
Checking presence of package libroar >= 1.0.12 ... no
Checking presence of package jack >= 0.120.1 ... 0.126.0
Checking presence of package libpulse ... 16.1
Checking presence of package libpipewire-0.3 ... 1.0.5
Checking presence of package libpipewire-0.3 >= 1.0.0 ... 1.0.5
Checking presence of package sdl >= 1.2.10 ... 1.2.68
Checking presence of package sdl2 >= 2.0.0 ... 2.30.6
Notice: SDL drivers will be replaced by SDL2 ones.
Checking presence of package Qt6Core >= 6.2 ... 6.4.2
Checking presence of package Qt6Gui >= 6.2 ... 6.4.2
Checking presence of package Qt6Widgets >= 6.2 ... 6.4.2
Checking presence of package Qt6Concurrent >= 6.2 ... 6.4.2
Checking presence of package Qt6Network >= 6.2 ... 6.4.2
Checking presence of package openssl >= 1.0.0 ... 3.0.13
Checking presence of package flac ... 1.4.3
Checking presence of package mbedtls >= 2.5.1 ... 2.28.8
Checking presence of package mbedx509 >= 2.5.1 ... 2.28.8
Checking presence of package mbedcrypto >= 2.5.1 ... 2.28.8
Notice: HID is disabled, libusb support will also be disabled.
Checking existence of -ldinput8 ... no
Checking existence of -ld3d9 ... no
Checking existence of -ldsound ... no
Checking existence of -ld3dx8 ... no
Checking existence of -ld3dx9 ... no
Checking presence of header file GL/gl.h ... yes
Checking existence of -lGL ... yes
Checking function cgCreateContext in -lCg -lCgGL ... yes
Checking presence of package zlib ... 1.3
Checking presence of package libavcodec >= 57 ... 60.31.102
Checking presence of package libavformat >= 57 ... 60.16.100
Checking presence of package libavdevice >= 57 ... 60.3.100
Checking presence of package libswresample >= 2 ... 4.12.100
Checking presence of package libavutil >= 55 ... 58.29.100
Checking presence of package libswscale >= 4 ... 7.5.100
Checking presence of header file libavutil/channel_layout.h ... yes
Checking function dlopen in -ldl ... yes
Checking presence of package gbm >= 9.0 ... 24.2.8-1ubuntu1~24.04.1
Checking presence of package libdrm ... 2.4.122
Checking presence of package vg ... no
Checking presence of package libudev ... 255
Checking presence of package libv4l2 ... 1.26.1
Checking presence of package freetype2 ... 26.1.20
Checking presence of package fontconfig ... 2.15.0
Checking presence of package x11 ... 1.8.7
Checking presence of package xcb ... 1.15
Checking presence of package xext ... 1.3.4
Checking presence of package xxf86vm ... 1.1.4
Checking presence of package xscrnsaver ... 1.2.3
Checking presence of package xi ... 1.8.1
Checking presence of package xinerama ... 1.1.4
Checking existence of -lXrandr ... yes
Checking presence of package xkbcommon >= 0.3.2 ... 1.6.0
Checking presence of package wayland-egl >= 10.1.0 ... 18.1.0
Checking presence of package wayland-cursor >= 1.12 ... 1.22.0
Checking presence of package wayland-protocols >= 1.32 ... 1.34
Checking presence of package wayland-scanner >= 1.12 ... 1.22.0
Could not open input file: No such file or directory
Error: Failed generating wayland protocols.
```
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `45764673c76fca3a95b8c4f3f4c4866051c545e7` and the full history behind it is present.
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
