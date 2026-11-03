# Locate the commit that introduced this regression

A regression was reported against `numpy/numpy`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
loops.c fails to compile from generated source on Westmere

The generated source `numpy/core/src/umath/loops.c` fails to compile on a fairly old Linux machine with Westmere CPU (with no AVX/AVX2 instructions).  The assembly file generated from `loops.c` contains a large amount of illegal instructions.

It seems that either the recent `numpy` isn't compatible with older CPUs, or there is a bug in configuring the generated code.



The full error output is too huge and here is the relevant beginning:

```
gcc: build/src.linux-x86_64-2.7/numpy/core/src/umath/loops.c                    
/tmp/cc9nF6h7.s: Assembler messages:                                            
/tmp/cc9nF6h7.s:43293: Error: suffix or operands invalid for `vpunpcklbw'       
/tmp/cc9nF6h7.s:43294: Error: suffix or operands invalid for `vpunpckhbw'       
/tmp/cc9nF6h7.s:43295: Error: suffix or operands invalid for `vpmullw'          
/tmp/cc9nF6h7.s:43296: Error: suffix or operands invalid for `vpshufb'          
/tmp/cc9nF6h7.s:43297: Error: suffix or operands invalid for `vpmullw'          
/tmp/cc9nF6h7.s:43298: Error: suffix or operands invalid for `vpshufb'          
/tmp/cc9nF6h7.s:43299: Error: suffix or operands invalid for `vpor'             
/tmp/cc9nF6h7.s:43301: Error: no such instruction: `vextracti128 $0x1,%ymm0,16(%
r8,%rdi)'
/tmp/cc9nF6h7.s:43535: Error: suffix or operands invalid for `vpmovsxbw'        
/tmp/cc9nF6h7.s:43536: Error: no such instruction: `vextracti128 $0x1,%ymm0,%xmm
0'
/tmp/cc9nF6h7.s:43537: Error: suffix or operands invalid for `vpmovsxwd'        
/tmp/cc9nF6h7.s:43538: Error: suffix or operands invalid for `vpmovsxbw'        
/tmp/cc9nF6h7.s:43539: Error: no such instruction: `vextracti128 $0x1,%ymm6,%xmm
0'
```

The compiler is GNU `gcc 5.2.0`.

CPU id:

```
vendor_id       : GenuineIntel
cpu family      : 6
model           : 47
model name      : Intel(R) Xeon(R) CPU E7- 4850  @ 2.00GHz
```

CPU flags:

```
flags           : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc arch_perfmon pebs bts rep_good xtopology nonstop_tsc aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2ap
```
```

## What you have

- `/testbed/repo` is a git clone of `numpy/numpy` truncated just after the regression was
  reported.  `HEAD` is `dbb70947b95b92abf3e48ef8be7bd3ab79489892` and the full history behind it is present.
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
