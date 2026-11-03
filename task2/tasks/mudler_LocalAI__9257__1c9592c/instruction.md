# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
backend libraries not found but present, fallback used instead of grpc but grpc called from backend

<!-- Thanks for helping us to improve LocalAI! We welcome all bug reports. Please fill out each area of the template so we can better help you. Comments like this will be hidden when you post but you can delete them if you wish. -->

**LocalAI version:**
localAI 4.x

**Environment, CPU architecture, OS, and Version:**
amd64, VM

**Describe the bug**
backend libraries not found

**To Reproduce**

cd backends/rocm-llama-cpp
./run.sh

ldd llama-cpp-grpc 
	linux-vdso.so.1 (0x00007f647be10000)
	libomp.so => not found
	libhipblas.so.2 => not found
	librocblas.so.4 => not found
	libamdhip64.so.6 => not found
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f647bcfc000)
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f647ba00000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f647bccf000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f647b80c000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f647be12000)

ldd llama-cpp-fallback 
	linux-vdso.so.1 (0x00007fc0a17c4000)
	libomp.so => not found
	libhipblas.so.2 => not found
	librocblas.so.4 => not found
	libamdhip64.so.6 => not found
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007fc0a16b0000)
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007fc0a1400000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007fc0a1683000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fc0a120c000)
	/lib64/ld-linux-x86-64.so.2 (0x00007fc0a17c6000)

ldd llama-cpp-rpc-server 
	linux-vdso.so.1 (0x00007f4359dbd000)
	libomp.so => not found
	libhipblas.so.2 => not found
	librocblas.so.4 => not found
	libamdhip64.so.6 => not found
	libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007f4359ca9000)
	libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007f4359a00000)
	libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007f4359c7c000)
	libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f435980c000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f4359dbf000)


**Expected behavior**
backend libraries found

**Logs**


**Additional context**
manually setting 
    LD_LIBRARY_PATH=/usr/local/rocm/lib
or
    LD_LIBRARY_PATH=/home/myuser/localai/backends/rocm-llama-cpp/lib
both fail because libc6.so is shipped separately yet the required libraries are not found

ls
ls: symbol lookup error: libc.so.6: undefined symbol: __nptl_change_stack_perm, version GLIBC_PRIVATE


see also output for run.sh is
.....

+ echo 'Using binary: llama-cpp-fallback'
Using binary: llama-cpp-fallback
+ exec /localai/backends/rocm-llama-cpp/lib/ld.so  /localai/backends/rocm-llama-cpp/llama-cpp-fallback
 /localai/backends/rocm-llama-cpp/llama-cpp-fallback: error while loading shared libraries: libhipblaslt.so.0: cannot open shared object file: No such file or directory
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1c9592c77ff9c253fe23250e490cc5c09f002f4d`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "mudler_LocalAI__9257__1c9592c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
