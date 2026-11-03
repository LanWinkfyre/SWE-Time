# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Eval bug: DGX Spark GB10 cluster crashing in RPC

### Name and Version

bob@spark-f713:~/llama.cpp/build/bin$ ./llama-server --version

built with GNU 13.3.0 for Linux aarch64

### Operating systems

Linux

### GGML backends

CUDA

### Hardware

DGX Spark GB10 + Grace Blackwell GPU (x2)

### Models

NVIDIA-Nemotron-3-Super-120B-A12B-UD-Q4_K_M
Qwen3-Coder-30B-A3B-Instruct-Q8_0

### Problem description & steps to reproduce

1. Launch `ggml-rpc-server` on node 2 with proper IP/port.
2. Launch  `llama-server` on node 1, passing "--rpc" option with proper IP/port.
4. `llama-server` interacts with `ggml-rpc-server`.
5. `ggml-rpc-server` crashes in ggml_backend_cuda_graph_compute().

- `./llama-server -m /home/bob/.cache/llmfit/models/NVIDIA-Nemotron-3-Super-120B-A12B-UD-Q4_K_M-00001-of-00003.gguf --jinja --alias nemotron3 --ctx-size 262144 --flash-attn on --host 0.0.0.0 --port 8001 --rpc 192.168.100.2:50052 --split-mode tensor`
- (also run with "--split-mode layer" and without "--split-mode")
- `./ggml-rpc-server -p 50052 --host 192.168.100.2`



_No response_

### Relevant log output

<details>
<summary>Logs</summary>
<!-- Copy-pasted short logs go into the "console" area here -->
...<br>
/home/bob/llama.cpp/ggml/src/ggml-cuda/ggml-cuda.cu:3927: GGML_ASSERT(ok) failed
[New LWP 38315]
[New LWP 38311]

This GDB supports auto-downloading debuginfo from the following URLs:
  <https://debuginfod.ubuntu.com>
Enable debuginfod for this session? (y or [n]) [answered N; input not from terminal]
Debuginfod has been disabled.
To make this setting permanent, add 'set debuginfod enabled off' to .gdbinit.
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/aarch64-linux-gnu/libthread_db.so.1".
0x0000f4a461307b74 in __GI___wait4 (pid=38322, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
warning: 30	../sysdeps/unix/sysv/linux/wait4.c: No such file or directory
#0  0x0000f4a461307b74 in __GI___wait4 (pid=38322, stat_loc=0x0, options=0, usage=0x0) at ../sysdeps/unix/sysv/linux/wait4.c:30
30	in ../sysdeps/unix/sysv/linux/wait4.c
#1  0x0000f4a4616e8b3c in ggml_print_backtrace () from /home/bob/llama.cpp/build/bin/libggml-base.so.0
#2  0x0000f4a4616e8ce0 in ggml_abort () from /home/bob/llama.cpp/build/bin/libggml-base.so.0
#3  0x0000f4a45f0910b4 in ggml_backend_cuda_graph_compute(ggml_backend*, ggml_cgraph*) () from /home/bob/llama.cpp/build/bin/libggml-cuda.so.0
#4  0x0000f4a4616ffdc4 in ggml_backend_graph_compute () from /home/bob/llama.cpp/build/bin/libggml-base.so.0
#5  0x0000f4a45ee5e590 in rpc_server::graph_compute(std::vector<unsigned char, std::allocator<unsigned char> > const&) () from /home/bob/llama.cpp/build/bin/libggml-rpc.so.0
#6  0x0000f4a45ee62b20 in rpc_serve_client(std::vector<ggml_backend*, std::allocator<ggml_backend*> > const&, char const*, std::shared_ptr<socket_t>) () from /home/bob/llama.cpp/build/bin/libggml-rpc.so.0
#7  0x0000f4a45ee64ea0 in ggml_backend_rpc_start_server () from /home/bob/llama.cpp/build/bin/libggml-rpc.so.0
#8  0x0000c95980c25a38 in main ()
[Inferior 1 (process 38310) detached]
Aborted (core dumped)
</details>

<!-- Long logs that you upload as files go here, outside the "console" area -->



Tested with unsloth-Qwen3.6-35BA3B-Q4-MTP.
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `e8f19cc0ad70a243c8012bf17b4be601abfc8ea2` and the full history behind it is present.
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
