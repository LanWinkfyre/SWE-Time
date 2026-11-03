# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
bad slicing and non-determinism in parse

I'm seeing a lot of non-determinism in `parse()` in Dyninst master.
Dyninst 13.0.0 had a fair amount of non-det in parse, but now master
is hopeless to get two runs to exactly agree 100%.

For example, running `parse()` on the `hpcstruct` binary 50 times, with
master I got 50 unique answers (as verified by md5sum).  13.0.0 would
have a consensus answer about 70-80% of the time with clusters of
other answers.

I've traced the problem in large part to inconsistent indirect jump table
analysis.  That is, there will be an indirect jump instruction (`jmp *%rdx`)
with a data race for the set of outgoing edges.

This is kinda serious, especially for `hpcstruct`.  Bogus edges in the
CFG produce bad and misleading output for hpcstruct.  There are
distorted loops, code that appears in multiple functions, plus it
makes it near impossible to keep a reference answer to test correctness.

The hpcstruct binary (as input to hpcstruct) is a decent stress test
for this because it pulls in code from a variety of sources: C++ maps,
Boost, XED, Dyninst, Intel TBB, OpenMP, etc.  It seems XED is
particularly good at causing problems.

Here are five examples.  I ran hpcstruct (including parse() with
dynininst openmp) at 24 threads analyzing itself on x86_64 and turned
on some knobs to dump the CFG (functions, blocks, edges, linemap and
inline sequences) as computed by Symtab and ParseAPI.  Then I looked
at the diffs of the debug output.

Note: I also tried this serially.  It was deterministic at one thread.
This suggests the problem is a data race instead of an algorithmic
mistake, which I guess is good news.

I've put the binary (`STRUCT`) along with objdump and a few runs on ufront:
```
/home/krentel/Dyninst-slicing
-rw-r--r-- 1 krentel users  28789586 Nov  3 10:58 Objdump
-rwxr-xr-x 1 krentel users  15404976 Nov  3 10:58 STRUCT
-rw-r--r-- 1 krentel users 141577782 Nov  3 10:58 out-2
-rw-r--r-- 1 krentel users 141369516 Nov  3 16:26 out-5
-rw-r--r-- 1 krentel users 141600114 Nov  3 10:58 out-ref
```

`out-ref` is the "reference" output that I got running hpcstruct
serially.  It's not guaranteed to be correct, but usually makes more
sense than the other runs where they differ.

The hpcstruct debug info (set `DEBUG_CFG_SOURCE` to 1 in `Struct.cpp`)
is pretty straightforward.  It just dumps the blocks, edges and inline
info as dyninst hands them to struct.

----------

(1) Sometimes the number of out edges from a block are different.

For example, with `hpcstruct` (STRUCT), comparing `out-ref` with
`out-2` look at address `0x4b8408`.

Objdump reports:
```
00000000004b8370 <xed3_capture_chain_ntluf_REG0_ZMM_N3_REG1_MASK1_REG2_ZMM_B3_IMM0_const1>:
  ...
  4b83f4:       77 1a                   ja     4b8410 
  4b83f6:       0f b6 53 53             movzbl 0x53(%rbx),%edx
  4b83fa:       48 8d 0d d3 49 13 00    lea    0x1349d3(%rip),%rcx
  4b8401:       48 63 14 91             movslq (%rcx,%rdx,4),%rdx
  4b8405:       48 01 ca                add    %rcx,%rdx
  4b8408:       ff e2                   jmp    *%rdx
```

`out-ref` reports 3 inline steps and 8 out edges for `0x4b8408`
```
stmt:  0x4b8408 (2)  l=18720  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'
   inline:  l=11635  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-op-chain-capture.h'
            p='xed3_capture_chain_ntluf_REG0_ZMM_R3_REG1_MASK1_REG2_ZMM_B3_IMM0_const1'
   inline:  l=11649  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-op-chain-capture.h'  p='xed3_capture_nt_ZMM_B3'
   inline:  l=18701  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'  p='xed3_capture_nt_ZMM_B3_32'

out edges:  0x4b8460 (indirect)  0x4b8480 (indirect)  0x4b8490 (indirect)  0x4b84a0 (indirect)
    0x4b84b0 (indirect)  0x4b84c0 (indirect)  0x4b84d0 (indirect)  0x4b84e0 (indirect)
```

`out-2` reports the same 3 inline steps but 18 out edges.
```
out edges:  0x4b8460 (indirect)  0x4b8480 (indirect)  0x4b8490 (indirect)  0x4b84a0 (indirect)
    0x4b84b0 (indirect)  0x4b84c0 (indirect)  0x4b84d0 (indirect)  0x4b84e0 (indirect)
    0x4b85b0 (indirect)  0x4b85d0 (indirect)  0x4b85e0 (indirect)  0x4b85f0 (indirect)
    0x4b8600 (indirect)  0x4b8610 (indirect)  0x4b8620 (indirect)  0x4b8630 (indirect)
    0x4b8640 (indirect)  0x4b8650 (indirect)
```

Note: `0x4b84e0` is the last out edge within the function at `0x4b8370`.
The other targets are in different functions and probably bogus.

They can't both be correct and certainly not the same fixed point.

In this case, this makes it look like `0x4b85b0` belongs to two
functions which creates havoc in hpcstruct/hpcprof and bad
presentation in hpcviewer.

----------

(2) Another example of (1).  This is between `out-ref` and `out-5` at
address `0x493406`, also in a XED function.

```
0000000000493380 <xed3_capture_nt_NELEM_FULLMEM>:
  ...
  4933f6:       77 26                   ja     49341e 
  4933f8:       48 8d 0d 4d 5b 15 00    lea    0x155b4d(%rip),%rcx 
  4933ff:       48 63 04 81             movslq (%rcx,%rax,4),%rax
  493403:       48 01 c8                add    %rcx,%rax
  493406:       ff e0                   jmp    *%rax
```

`out-ref` has 13 out edges.
```
stmt:  0x493406 (2)
out edges:  0x49341e (indirect)  0x493428 (indirect)  0x493430 (indirect)  0x493438 (indirect)
    0x493440 (indirect)  0x493460 (indirect)  0x49349c (indirect)  0x4934f4 (indirect)
    0x4934fc (indirect)  0x493504 (indirect)  0x49350c (indirect)  0x493514 (indirect)
    0x493535 (indirect)
```

But `out-5` has only has 6.
```
stmt:  0x493406 (2)
out edges:  0x49341e (indirect)  0x493428 (indirect)  0x493430 (indirect)  0x493438 (indirect)
    0x493440 (indirect)  0x493460 (indirect)
```

Again, all the extra edges are at the high end.  `0x49349c` is not
even the start of an instruction.  And the rest are past the end of
the `493380` function.

In this case, it's the reference output that looks suspicious.

----------

(3) Sometimes at an indirect branch, one run will miss all outgoing
edges entirely (zero outgoing edges) or have just one edge to the
sink (0xffffffffffffffff).

Again with `out-ref` vs `out-5`, at address `0x4934fe`.

```
00000000004934c0 <xed3_capture_nt_NELEM_HALFMEM>:
  ...
  4934ee:       77 30                   ja     493520
  4934f0:       48 8d 0d d9 5a 15 00    lea    0x155ad9(%rip),%rcx
  4934f7:       48 63 04 81             movslq (%rcx,%rax,4),%rax
  4934fb:       48 01 c8                add    %rcx,%rax
  4934fe:       ff e0                   jmp    *%rax
```

`out-ref`
```
stmt:  0x4934fe (2)  l=14762  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'
out edges:  0xffffffffffffffff (indirect)
```

`out-5` finds 14 out edges
```
stmt:  0x4934fe (2)  l=14762  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'
out edges:  0x49349c (indirect)  0x4934fc (indirect)  0x493504 (indirect)  0x49350c (indirect)
    0x493514 (indirect)  0x493520 (indirect)  0x49353c (indirect)  0x493541 (indirect)
    0x493578 (indirect)  0x493580 (indirect)  0x493588 (indirect)  0x493590 (indirect)
    0x493598 (indirect)  0x4935b9 (indirect)
```

I don't know why one run would have only an edge to the sink and the
other finds 14 edges.  Maybe there's a data race in the linked list
causing one to reset the list to empty.  Maybe the real problem is
elsewhere and this is just a symptom.

----------

(4) Here's one with an empty list outgoing edges at `0x4b56d4`

```
  4b56b4:       e9 67 ff ff ff          jmp    4b5620
  4b56b9:       0f 1f 80 00 00 00 00    nopl   0x0(%rax)
  4b56c0:       41 b8 ac 00 00 00       mov    $0xac,%r8d
  4b56c6:       0f b6 47 5b             movzbl 0x5b(%rdi),%eax
  4b56ca:       ba ac 00 00 00          mov    $0xac,%edx
  4b56cf:       66 44 89 47 7e          mov    %r8w,0x7e(%rdi)
  4b56d4:       e9 47 ff ff ff          jmp    4b5620
```

`out-ref` has no out edges
```
block:
stmt:  0x4b56c0 (6)  l=17225  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'
...
stmt:  0x4b56d4 (5)  l=17227  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'
   inline:  l=13029  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-op-chain-capture.h'  p='xed3_capture_nt_MASK_R'
   inline:  l=17225  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'  p='xed3_operand_set_outreg'
out edges:
```

But `out-5` finds the direct edge.
```
stmt:  0x4b56d4 (5)  l=17227  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'
   inline:  l=13029  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-op-chain-capture.h'  p='xed3_capture_nt_MASK_R'
   inline:  l=17225  f='/home/krentel/unit/hpctoolkit/builddir-orig/subprojects/xed-2023.10.11/xed3-nt-capture.h'  p='xed3_operand_set_outreg'
out edges:  0x4b5620 (direct)
```

This is especially strange because it's a direct edge.
You don't need any complicated slicing.
So why does one run, the reference run miss it?

----------

(5) Finally, often times the out edge to the sink is repeated.

Address `0x436029`, objdump has:
```
0000000000435fb0 <_ZN3tbb6detail2d213hash_map_baseINS0_2d113tbb_allocatorISt4pairIKmPN7Dyninst8Par
seAPI8GPUBlockEEEENS3_13spin_rw_mutexEE14enable_segmentEmb>:
  ...
  436021:       5b                      pop    %rbx
  436022:       5d                      pop    %rbp
  436023:       41 5c                   pop    %r12
  436025:       41 5d                   pop    %r13
  436027:       41 5e                   pop    %r14
  436029:       c3                      ret
```

`out-ref` has 2 edges to the sink
```
stmt:  0x436029 (1)  l=215  f='/home/krentel/Spack/install/linux-broadwell/intel-tbb-2022.0.0-w3zhzmgxuu4uuqstenqkhdzjtnhmqxel/include/oneapi/tbb/concurrent_hash_map.h'
out edges:  0x436112 (return, interproc)  0x4368fe (return, interproc)
    0xffffffffffffffff (return, interproc)  0xffffffffffffffff (return, interproc)
```

But out-5 has only one:
```
stmt:  0x436029 (1)  l=215  f='/home/krentel/Spack/install/linux-broadwell/intel-tbb-2022.0.0-w3zhzmgxuu4uuqstenqkhdzjtnhmqxel/include/oneapi/tbb/concurrent_hash_map.h'
out edges:  0x436112 (return, interproc)  0x4368fe (return, interproc)  0xffffffffffffffff (return, interproc)
```

This is maybe a bit sloppy and shouldn't cause hpcstruct any trouble.
But it's non-deterministic and maybe it's an indication of a more
serious data race.  It even happens serially.


**System (please complete the following information):**
Linux x86_64, RHEL 8.10, gcc 13.4.0, glibc 2.28
Dyninst master at 5867d62f800128 as of Oct 15, 2025
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `e6480522b30638faf324332f209d246adf9046cf`.  There
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
{"case_id": "dyninst_dyninst__2050__e648052",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
