# Locate the commit that introduced this regression

A regression was reported against `mpv-player/mpv`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
BT.2020 HDR video is washed out on dmabuf-wayland vo when shown on SDR monitor

### mpv Information



### Other Information

```text
- Linux version: Arch Linux
- Kernel Version: 6.16.8-arch1-1
- GPU Model: 63:00.0 VGA compatible controller [0300]: Advanced Micro Devices, Inc. [AMD/ATI] Rembrandt [Radeon 680M] [1002:1681] (rev d8)
- Mesa/GPU Driver Version: Mesa 25.2.3-arch1.2
- Window Manager and Version: kwin 6.4.5-3
- Source of mpv: archlinuxcn repo (https://github.com/archlinuxcn/repo/tree/master/archlinuxcn/mpv-git)
- Latest known working version: 0.40.0
- Issue started after the following happened: play an HDR BT.2020 video
```

### Reproduction Steps

I am using a LG 27UL550-W monitor in SDR mode. Desktop environment is KDE Plasma 6.4.5 (Wayland), without setting ICC in KDE System Settings.

Download https://www.youtube.com/watch?v=T-rxE5vKlkg (with yt-dlp video format 335) and open it with `mpv ~/Videos/'Trailer 2 ｜ One Battle After Another ｜ 4K HDR ｜ Dolby 5.1 #4K #10bit #Surround #Flat [T-rxE5vKlkg].webm' --vo=dmabuf-wayland --mute --pause --start=36 --no-config --hwdec=vaapi` will show a washed out image.

While investigating, I tried setting WAYLAND_DEBUG environment variable to see the events, (full log here: [mpv-wayland-debug.log](https://github.com/user-attachments/files/22499722/mpv.log)) and noticed that `wp_color_management_surface_v1#45.set_image_description` only happens **after** `wl_surface#6.commit`, could it be related to the washed out image?

```
(...)
[3518704.473] {Default Queue}  -> wp_color_representation_surface_v1#63.set_coefficients_and_range(6, 2)
[3518704.475] {Default Queue}  -> wp_color_representation_surface_v1#63.set_chroma_location(1)
[3518704.478] {Default Queue}  -> wl_surface#6.attach(wl_buffer#60, 0, 0)
[3518704.481] {Default Queue}  -> wl_surface#6.damage_buffer(0, 0, 1920, 1038)
[3518704.486] {Default Queue}  -> wl_shm_pool#50.create_buffer(new id wl_buffer#64, 0, 1920, 1038, 7680, 0)
[3518704.727] {Default Queue}  -> wl_surface#7.commit()
[3518704.731] {Default Queue}  -> wl_surface#6.commit()  <-- This one happens...
[3518704.733] {Default Queue}  -> wl_surface#5.commit()
[3518704.984] {Display Queue} wl_display#1.delete_id(57)
(...)
[3518705.000] {Display Queue} wl_display#1.delete_id(58)
[3518705.002] {Default Queue} wp_image_description_v1#62.ready(171)
[3518705.006] {Default Queue}  -> wp_color_management_surface_v1#45.set_image_description(wp_image_description_v1#62, 0)   <-- before this
[3518705.009] {Default Queue}  -> wp_image_description_v1#62.destroy()
[3518705.012] {Default Queue} wl_buffer#55.release()
(...)
```

### Expected Behavior

Compare to gpu-next:

command: `mpv ~/Videos/'Trailer 2 ｜ One Battle After Another ｜ 4K HDR ｜ Dolby 5.1 #4K #10bit #Surround #Flat [T-rxE5vKlkg].webm' --vo=gpu-next --mute --pause --start=36 --no-config --hwdec=vaapi`

![Image](https://github.com/user-attachments/assets/2e4bacc7-cc92-401e-aeec-30102e874960)

### Actual Behavior

The vo=dmabuf-wayland image looks washed out like this:

![Image](https://github.com/user-attachments/assets/3ac4e916-827b-4b90-a5e1-f5c5557d9651)

### Log File

[output.txt](https://github.com/user-attachments/files/22499635/output.txt)

### Sample Files

https://drive.google.com/file/d/1252P04j0izxKbG87jgVbYAOSi-9PofQF/view?usp=sharing

### I carefully read all instruction and confirm that I did the following:

- [x] I tested with the latest mpv version to validate that the issue is not already fixed.
- [x] I provided all required information including system and mpv version.
- [x] I produced the log file with the exact same set of files, parameters, and conditions used in "Reproduction Steps", with the addition of `--log-file=output.txt`.
- [x] I produced the log file while the behaviors described in "Actual Behavior" were actively observed.
- [x] I attached the full, untruncated log file.
- [x] I attached the backtrace in the case of a crash.

> > > Given that mpv 1:0.40.0-6 with vo=dmabuf-wayland shows mostly the same image as vo=gpu-next, I think kwin's tonemapping is doing ok here 🤔
> > 
> > 
> > Could you bisect mpv to find when it regressed? This would be the fastest way to fix this.
> 
> Will do.
```

## What you have

- `/testbed/repo` is a git clone of `mpv-player/mpv` truncated just after the regression was
  reported.  `HEAD` is `be98b35c89b42c6f094de4a97ee0a926559a5fa4` and the full history behind it is present.
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
