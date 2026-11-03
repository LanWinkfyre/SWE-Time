# Locate the commit that introduced this regression

A regression was reported against `bazelbuild/bazel`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Bazel CI: C++ compilation in some projects are broken on Windows

https://buildkite.com/bazel/bazel-with-downstream-projects-bazel/builds/498

From rules_typescript:
```

ERROR: C:/users/b/_bazel_b/s2xmyw5r/external/com_google_protobuf/BUILD:70:1: Couldn't build file external/com_google_protobuf/_objs/protobuf_lite/generated_message_util.obj: C++ compilation of rule '@com_google_protobuf//:protobuf_lite' failed (Exit 2)
--
  | cl : Command line error D8021 : invalid numeric argument '/Wwrite-strings'

```

From TensorFlow:
```
ERROR: C:/users/b/_bazel_b/vpozbdwp/external/protobuf_archive/BUILD:70:1: Couldn't build file external/protobuf_archive/_objs/protobuf_lite/common.obj: C++ compilation of rule '@protobuf_archive//:protobuf_lite' failed (Exit 2): cl.exe failed: error executing command
--
  | cd C:/users/b/_bazel_b/vpozbdwp/execroot/org_tensorflow
  | SET INCLUDE=C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\INCLUDE;C:\Program Files (x86)\Windows Kits\10\include\10.0.10240.0\ucrt;C:\Program Files (x86)\Windows Kits\8.1\include\shared;C:\Program Files (x86)\Windows Kits\8.1\include\um;C:\Program Files (x86)\Windows Kits\8.1\include\winrt;
  | SET PATH=C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\BIN\amd64;C:\Windows\Microsoft.NET\Framework64\v4.0.30319;C:\Windows\Microsoft.NET\Framework64\;C:\Program Files (x86)\Windows Kits\8.1\bin\x64;C:\Program Files (x86)\Windows Kits\8.1\bin\x86;;C:\Windows\system32
  | SET PWD=/proc/self/cwd
  | SET PYTHON_BIN_PATH=C:/python3/python.exe
  | SET PYTHON_LIB_PATH=C:/python3/lib/site-packages
  | SET TEMP=D:\temp
  | SET TF_DOWNLOAD_CLANG=0
  | SET TF_NEED_CUDA=0
  | SET TF_NEED_OPENCL_SYCL=0
  | SET TF_NEED_ROCM=0
  | SET TMP=D:\temp
  | C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64/cl.exe /nologo /DCOMPILER_MSVC /DNOMINMAX /D_WIN32_WINNT=0x0601 /D_CRT_SECURE_NO_DEPRECATE /D_CRT_SECURE_NO_WARNINGS /bigobj /Zm500 /EHsc /wd4351 /wd4291 /wd4250 /wd4996 /Iexternal/protobuf_archive /Ibazel-out/x64_windows-opt/genfiles/external/protobuf_archive /Ibazel-out/x64_windows-opt/bin/external/protobuf_archive /Iexternal/bazel_tools /Ibazel-out/x64_windows-opt/genfiles/external/bazel_tools /Ibazel-out/x64_windows-opt/bin/external/bazel_tools /Iexternal/protobuf_archive/src /Ibazel-out/x64_windows-opt/genfiles/external/protobuf_archive/src /Ibazel-out/x64_windows-opt/bin/external/protobuf_archive/src /showIncludes /MD /O2 /Oy- /DNDEBUG /wd4117 -D__DATE__="redacted" -D__TIMESTAMP__="redacted" -D__TIME__="redacted" /Gy /Gw -w -w -DHAVE_PTHREAD -Wall -Wwrite-strings -Woverloaded-virtual -Wno-sign-compare -Wno-unused-function -Wno-writable-strings /Fobazel-out/x64_windows-opt/bin/external/protobuf_archive/_objs/protobuf_lite/common.obj /c external/protobuf_archive/src/google/protobuf/stubs/common.cc
  | cl : Command line error D8021 : invalid numeric argument '/Wwrite-strings'

```



@scentini @mhlopko Should rollback first?
```

## What you have

- `/testbed/repo` is a git clone of `bazelbuild/bazel` truncated just after the regression was
  reported.  `HEAD` is `cffe0e30e4949dbf2a68fb6f2747ffe14333c8a7` and the full history behind it is present.
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
