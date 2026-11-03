# Locate the commit that introduced this regression

A regression was reported against `libretro/RetroArch`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
fif_libretro (Fix-It Felix Jr.) compatibility issues (Debian Retroarch armhf)

## Description
The core 'fif_libretro.so', the libretro core for the promotional Fix-It Felix Jr. arcade game licensed for AtGames cabinets and plug-n-play systems (originally developed by Code Mystics for Disney's promotional cabinets), crashes with a segmentation fault upon attempting to load with RetroArch for the armhf Linux platform (fif_libretro.so is a 32-bit ARMv8 ELF file).

### Expected behavior
Pictured is the game running properly under Ludo, another libretro frontend that works on armhf Linux platforms:
![image](https://github.com/libretro/RetroArch/assets/19103643/8b6df868-22d6-45ea-98db-42e7cfe85404)

### Actual behavior

Whenever I attempt to load fif_libretro.so, pointing it to the fif.rom dummy file (all actual game functionality is via the core, with assets loaded from the directory that contains fif.rom), it crashes with the following log output:

It's worth noting that I've been unable to get Retroarch's actual frontend GUI working under this particular configuration without unusable levels of lag (it always throws a libEGL error, which is another issue entirely), but I was able to verify that it actually works by using the command line to launch the mgba core directly with a test ROM.

### Steps to reproduce the bug

You are going to need to install Debian Testing ARM64 onto qemu-system-aarch64's generic 'virt' machine type. This is a painful experience that will likely involve switching to TTY3 multiple times to fix broken packages on the fly, as it will often take multiple attempts for dpkg to actually install all of the selected system packages without crashing mid LZMA extraction. After that, you are going to need to add the armhf platform to your system's multiarch configuration; merely installing a Debian armhf system is unsuitable, as Debian armhf targets ARMv7 as opposed to 32-bit ARMv8 like we want. Finally, install libretro:armhf, try to launch the fif_libretro core, and watch it segfault.

Here's the QEMU launch string that got everything _mostly_ working for me (even getting it to show the mouse cursor was an adventure):
```
qemu-system-aarch64 -machine virt,gic-version=max -cpu cortex-a53 -m 4G -smp 4 -netdev user,id=vnet,hostfwd=:127.0.0.1:0-:22 -device virtio-net-pci,netdev=vnet -drive file=harddisk.img,if=none,id=drive0,cache=writeback -device virtio-blk,drive=drive0,bootindex=0 -drive file=flash0.img,format=raw,if=pflash -drive file=flash1.img,format=raw,if=pflash -device virtio-gpu-pci -device qemu-xhci -device usb-kbd -device usb-tablet -display sdl,show-cursor=on
```
flash0.img is the AArch64 EFI image, flash1.img is a 64mb blank img for EFI vars, and harddisk.img is self explanatory (I advise at least 10gigs for the image). You're also going to need to specify install media, of course (I used the arm64 netinst iso).

As for _getting_ AtGames's version of Fix-It Felix Jr. (NOT the leaked alpha build for Windows)..... uhhhhhh........... good luck. Or you could buy an overpriced AtGames Legends Flashback and telnet into it to grab the files, I guess.

### Version/Commit



### Environment information

- OS: Linux debian-arm64 6.5.0-1-arm64 # 1 SMP Debian 6.5.3-1 (2023-09-13) aarch64 GNU/Linux




While I'm not really a very experienced programmer, so I don't really know what this commit actually does, I think it might be useful if I explained what the fif_libretro core requires in terms of files in order to run, since this seems to have to do with file paths.

fif_libretro.so is a core with no accompanying info file that takes a "rom" in the form of `fif.rom`; however, fif.rom is just a text file containing the plaintext 'FIF', so all it effectively is is a dummy file that serves as a way for the core to receive the directory with the actual image and sound assets in it, of which there are the following (SHA-1 hashes included):
```
SHA-1:
709f2f1a9147d9987a00c2c86ad1beced4ed4b75  ./fif_libretro.so
7a40f13a4f3cab9348f71cef4f3cbe155eadcb4f  ./res_fif/controls.log
2314358705f32d68c8709a990e724ecef3ed7b4c  ./res_fif/fif.rom
74f346a151e16e479de68e7ede99f6077749971a  ./res_fif/fif.rom.l.png
1f764f5f5b4387dd7853719b707aa5e852672108  ./res_fif/fif.rom.png
3fac5a8704d8f97e378152132e7e6ceb3288940f  ./res_fif/fif.rom.s.png
34a5dca2810f31ea7336b167b2e89dfba953db94  ./res_fif/sound0.wav
c9e41e0a3ef7b8b99bc04922135d4d9e772e0b8c  ./res_fif/sound1.wav
fb0fcd30c2736faec27cb2e6ae392c0ba997204f  ./res_fif/sound10.wav
f4fe6d07446e633d327fa0b5e8f77b51812236d9  ./res_fif/sound11.wav
c30eab4db02adf7be7fe4f1fc8bffd5b949e292c  ./res_fif/sound12.wav
c60445a5afc41fa1c7306e494de3d977c1860054  ./res_fif/sound13.wav
43619830a69d1541c432afcb27937ee928668e79  ./res_fif/sound14.wav
393f02665bccc12c71d78c8b406a81b623ff660d  ./res_fif/sound15.wav
9f3146264532fe42083fdfc5beef902046a91d20  ./res_fif/sound16.wav
56aa52bb0032aaa9edcdfe476b7af853b0a873d7  ./res_fif/sound17.wav
dba72e4253047894170d7b1b4fa48ea7f9b74f32  ./res_fif/sound18.wav
3517443234d3d75e485e23607fc34b699d5700d1  ./res_fif/sound19.wav
d296e8eef2059c6d2b00a49f78ada9828e6fb395  ./res_fif/sound2.wav
3bbd8ca70019b2123143d6397732b5877c5fc304  ./res_fif/sound20.wav
022138961a374d4eda7a133796b476edf87cb3b7  ./res_fif/sound21.wav
a89280408c43b5624b2ff4c84cbe66f1d83ddd18  ./res_fif/sound22.wav
8401b37e7bcaa4eef7caac2c3ef05a47c0f29847  ./res_fif/sound23.wav
2798b239ce23a22847cda2936cdfbb00e280b395  ./res_fif/sound24.wav
2bed76ffe0e3aa7137b4611b10dac1296dc6ffee  ./res_fif/sound25.wav
a93a3593b729444591f616afb981f454e2177a0c  ./res_fif/sound26.wav
5effb7b0fd79033973d7a66601cfe589a65893c2  ./res_fif/sound27.wav
0f0043be3fb2b97e207ee15684d8fb1f12fa9f3d  ./res_fif/sound28.wav
63a43994cc3a8fd92011e5a3b5d1ba8d501d07a5  ./res_fif/sound29.wav
404de5cb7d6a56ab9a17405e9241494693f79021  ./res_fif/sound3.wav
8f75836a9ba115b77c1e1002560b2896c62b61af  ./res_fif/sound30.wav
672ba3d47cdd654f82b8ee6c84572ee20ae7117c  ./res_fif/sound31.wav
a44af75d16a9e2f79d1dcead24dba35001913b09  ./res_fif/sound4.wav
6ecb91ac9534eaaa4069a043661c9c16e21942d2  ./res_fif/sound5.wav
66365bd6dc650d714547cfd46278da692b40fe22  ./res_fif/sound6.wav
ed09b930615429362628cde3713ec31cd2ce1a31  ./res_fif/sound7.wav
e21920b85c2edae9e7614251e0cf90b808de0072  ./res_fif/sound8.wav
1bd8cb6c168db29ecfa73e6e776277af21166579  ./res_fif/sound9.wav
3bd2ad5d0d481b813b00024cb0e290133238c5ba  ./res_fif/texture2.bmp
```
If any further info on the core is needed, I'm all up for answering any questions or doing any tests that I can, since this is a seriously hard file to acquire (although is IS out there).

EDIT: Also, since we now know where the breaking change was introduced, should this issue get a name change, and maybe some tags?
```

## What you have

- `/testbed/repo` is a git clone of `libretro/RetroArch` truncated just after the regression was
  reported.  `HEAD` is `ce6a00b4955365a729fbb0a64f5de9c5cfc1ca10` and the full history behind it is present.
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
