# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
retroarch.exe stopped working (intel HD 3000)

Hello guys, i am having trouble with the latest version of Retroarch.

Retroarch 1.4.1 crashes directly when opened. 
Error message retroarch.exe stopped working.

Version 1.3.6 runs fine and reconizes the HD 3000 graphics drivers.
When i run 1.4.1 it crashes immediatly 

I am running Windows 10 home 64 bit. 
I have tested both the 32bit and the 64 bit versions, makes no difference.  
I am running it local, not using RDP.

The hardware is an Acer W700 tablet running Windows 10 home 1607 with all updates

Intel(R) Core(TM) i3-2375M CPU @ 1.50GHz
Intel HD Graphics 3000
Driver version 10.17.10.4229
Also tested with version 9.17.10.4229 same issue


Here is the debug log.

> > Intel(R) Core(TM) i3-2375M CPU @ 1.50GHz

> RetroArch [INFO] :: === Build =======================================
> Capabilities: MMX MMXEXT SSE1 SSE2 SSE3 SSSE3 SSE4 SSE4.2 AVX
> Built: Feb 2 2017
> RetroArch [INFO] :: Version: 1.4.1

> RetroArch [INFO] :: =================================================
> RetroArch [INFO] :: Loading default config.
> RetroArch [INFO] :: Environ SET_PIXEL_FORMAT: RGB565.
> RetroArch [INFO] :: Redirecting save file to "C:\emulation\retro arch 1.41\saves.srm".
> RetroArch [INFO] :: Redirecting savestate to "C:\emulation\retro arch 1.41\states.state".
> RetroArch [INFO] :: Version of libretro API: 1
> RetroArch [INFO] :: Compiled against API: 1
> RetroArch [INFO] :: Set audio input rate to: 29970.03 Hz.
> RetroArch [INFO] :: Video @ 960x720
> RetroArch [INFO] :: Found GL context: wgl
> RetroArch [INFO] :: Detecting screen resolution 1920x1080.
> RetroArch [ERROR] :: [WGL]: wglCreateContextAttribsARB not supported.
> RetroArch [INFO] :: [GL]: Vendor: Microsoft Corporation, Renderer: GDI Generic.
> RetroArch [INFO] :: [GL]: Version: 1.1.0.

Here is the log of the working 1.3.6 on the same system.

> RetroArch [INFO] :: === Build =======================================
> Capabilities: MMX MMXEXT SSE1 SSE2 SSE3 SSSE3 SSE4 SSE4.2 AVX
> Built: Aug 4 2016
> RetroArch [INFO] :: Version: 1.3.6

> RetroArch [INFO] :: =================================================
> RetroArch [INFO] :: Config: loading config from: C:\emulation\retro arch 1.36\retroarch.cfg.
> RetroArch [INFO] :: Resetting undo buffers.
> RetroArch [INFO] :: Environ SET_PIXEL_FORMAT: RGB565.
> RetroArch [INFO] :: Version of libretro API: 1
> RetroArch [INFO] :: Compiled against API: 1
> RetroArch [INFO] :: Set audio input rate to: 29975.00 Hz.
> RetroArch [INFO] :: Found shader "C:\emulation\retro arch 1.36\shaders\retroarch.cgp"
> RetroArch [INFO] :: Found shader "C:\emulation\retro arch 1.36\shaders\retroarch.glslp"
> RetroArch [INFO] :: Video @ 960x720
> RetroArch [INFO] :: Found GL context: wgl
> RetroArch [INFO] :: Detecting screen resolution 1920x1080.
> RetroArch [INFO] :: [WGL]: wglSwapInterval(1)
> RetroArch [INFO] :: [GL]: Vendor: Intel, Renderer: Intel(R) HD Graphics 3000.
> RetroArch [INFO] :: [GL]: Version: 3.1.0 - Build 9.17.10.4229.
> RetroArch [INFO] :: Querying GL extension: ARB_ES2_compatibility => doesn't exist
> RetroArch [INFO] :: Querying GL extension: ARB_sync => exists
> RetroArch [INFO] :: Querying GL extension: ARB_texture_float => exists
> RetroArch [INFO] :: Querying GL extension: EXT_texture_sRGB => exists
> RetroArch [INFO] :: Querying GL extension: ARB_framebuffer_sRGB => exists
> RetroArch [INFO] :: [GL]: Supported extensions:


If more info is required  i am happy to help.

<bountysource-plugin>

---
Want to back this issue? **[Post a bounty on it!](https://www.bountysource.com/issues/41729458-retroarch-exe-stopped-working-intel-hd-3000?utm_campaign=plugin&utm_content=tracker%2F296058&utm_medium=issues&utm_source=github)** We accept bounties via [Bountysource](https://www.bountysource.com/?utm_campaign=plugin&utm_content=tracker%2F296058&utm_medium=issues&utm_source=github).
</bountysource-plugin>

I have been bisecting till there isn't a single version left to test, with no luck, it still crashes directly after loading, while on my nvidia machine's it runs without issue. Even the 1.3.5 which i build crashes.






Has there been a change in the way retroarch is compiled since 1.3.6 ?

Please note that i am by no means a programmer, just a guy who read the above tutorials to compile his first program since "the game of life" in turbo pascal at school.
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `74d29c4b40fff7e6afc5e0258f79294bd68fbaa6` and the full history behind it is present.
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
