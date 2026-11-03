# Locate the commit that introduced this regression

A regression was reported against `ggml-org/llama.cpp`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
w64devkit build segfaults at 0xFFFFFFFFFFFFFFFF

Steps to reproduce:
1. Install latest w64devkit
2. Build with `make LLAMA_DEBUG=1`
3. Simply run `./main`, regardless of whether you have a model in the default location (I don't)

50% of the time, it will fail. I cannot reproduce it if I build with MSYS2's mingw-w64 toolchain instead.



~~If cv2pdb is to be trusted~~ (confirmed below), the crash happens here:


Something is going wrong before that function call:
```
    llama_model * model  = llama_load_model_from_file(params.model.c_str(), lparams);
00007FF7CBE59448  mov         rax,qword ptr [params]  
00007FF7CBE5944F  add         rax,0C8h  
00007FF7CBE59455  mov         rcx,rax  
00007FF7CBE59458  call        _M_range_check+0F70h (07FF7CBEA0340h)  
00007FF7CBE5945D  mov         rcx,rax  
00007FF7CBE59460  vmovdqu     ymm0,ymmword ptr [lparams]  
00007FF7CBE59465  vmovdqa     ymmword ptr [rbp-60h],ymm0  <-- segfault is here
00007FF7CBE5946A  vmovdqu     ymm0,ymmword ptr [rbp+10h]  
00007FF7CBE5946F  vmovdqa     ymmword ptr [rbp-40h],ymm0  
00007FF7CBE59474  lea         rax,[rbp-60h]  
00007FF7CBE59478  mov         rdx,rax  
00007FF7CBE5947B  call        llama_load_model_from_file (07FF7CBE4B9D7h)
```
rbp is 0x0000007CA91FE0D0, so I'm not sure where 0xFFFFFFFFFFFFFFFF comes from. And it's a read violation, but that instruction is only reading from a register.
```

## What you have

- `/testbed/repo` is a git clone of `ggml-org/llama.cpp` truncated just after the regression was
  reported.  `HEAD` is `8afe2280009ecbfc9de2c93b8f41283dc810609a` and the full history behind it is present.
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
