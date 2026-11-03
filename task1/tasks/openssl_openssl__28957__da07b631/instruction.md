# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Illegal hardware instruction when computing SHA256 on x86_64 (x32 ABI)

Doing simple `echo | openssl sha256` results in illegal hardware instruction with `openssl 3.6.0` and `linux-x32` target. Apparently AVX codepath is taken even though host does not support AVX:
```
Program terminated with signal SIGILL, Illegal instruction.
#0  sha256_block_data_order_avx () at crypto/sha/sha256-x86_64.s:3127
3127            vzeroupper
(gdb) bt
#0  sha256_block_data_order_avx () at crypto/sha/sha256-x86_64.s:3127
#1  0xf73b36cd in SHA256_Final (md=md@entry=0x17f6610 "\n", c=c@entry=0x1804a50) at include/crypto/md32_common.h:245
#2  0xf742652b in sha256_internal_final (ctx=0x1804a50, out=0x17f6610 "\n", outl=0xfffbf7d8, outsz=32) at providers/implementations/digests/sha2_prov.c:71
#3  0xf72470c3 in EVP_DigestFinal_ex (ctx=ctx@entry=0x17f3600, md=md@entry=0x17f6610 "\n", isize=isize@entry=0xfffbf808) at crypto/evp/digest.c:468
#4  0xf724027f in md_gets (bp=<optimized out>, buf=0x17f6610 "\n", size=8192) at crypto/evp/bio_md.c:218
#5  0xf717e14e in BIO_gets (b=b@entry=0x1804990, buf=buf@entry=0x17f6610 "\n", size=size@entry=8192) at crypto/bio/bio_lib.c:577
#6  0x00435a80 in do_fp (out=out@entry=0x18049f0, buf=buf@entry=0x17f6610 "\n", bp=bp@entry=0x1804990, sep=sep@entry=0, binout=binout@entry=0, xoflen=xoflen@entry=0, key=0x0, sigin=0x0, 
    siglen=0, sig_name=0x0, md_name=0x1800470 "SHA2-256", file=0x496cdb "stdin") at apps/dgst.c:682
#7  0x00436c9b in dgst_main (argc=0, argv=0xfffbfc1c) at apps/dgst.c:456
#8  0x00448f8b in do_cmd (prog=prog@entry=0x17f5710, argc=argc@entry=1, argv=argv@entry=0xfffbfc18) at apps/openssl.c:486
#9  0x0041cdd2 in main (argc=<optimized out>, argv=<optimized out>) at apps/openssl.c:364
```

<details><summary>cpuid | grep -i avx</summary>

```
      AVX: advanced vector extensions         = false                                          
      AVX2: advanced vector extensions 2       = false                                                                                                                                         
      AVX512F: AVX-512 foundation instructions = false                                         
      AVX512DQ: double & quadword instructions = false                                         
      AVX512IFMA: integer fused multiply add   = false                                                                                                                                         
      AVX512PF: prefetch instructions          = false                                                                                                                                         
      AVX512ER: exponent & reciprocal instrs   = false                                                                                                                                         
      AVX512CD: conflict detection instrs      = false                                                                                                                                         
      AVX512BW: byte & word instructions       = false                                                                                                                                         
      AVX512VL: vector length                  = false                                                                                                                                         
      AVX512VBMI: vector byte manipulation     = false                                                                                                                                         
      AVX512_VBMI2: byte VPCOMPRESS, VPEXPAND  = false                                         
      AVX512_VNNI: neural network instructions = false                                                                                                                                         
      AVX512_BITALG: bit count/shiffle         = false                                   
      AVX512: VPOPCNTDQ instruction            = false                                         
      AVX512_4VNNIW: neural network instrs     = false                                                                                                                                         
      AVX512_4FMAPS: multiply acc single prec  = false               
      AVX512_VP2INTERSECT: intersect mask regs = false                                         
      AVX512_FP16: fp16 support                = false            
         AVX state                            = false                                          
         AVX-512 opmask                       = false                                                                                                                                          
         AVX-512 ZMM_Hi256                    = false                                          
         AVX-512 Hi16_ZMM                     = false               
      AVX: advanced vector extensions         = false                        
      AVX2: advanced vector extensions 2       = false                                         
      AVX512F: AVX-512 foundation instructions = false           
      AVX512DQ: double & quadword instructions = false          
      AVX512IFMA: integer fused multiply add   = false                     
      AVX512PF: prefetch instructions          = false                                         
      AVX512ER: exponent & reciprocal instrs   = false                                         
      AVX512CD: conflict detection instrs      = false                                         
      AVX512BW: byte & word instructions       = false
      AVX512VL: vector length                  = false                                         
      AVX512VBMI: vector byte manipulation     = false            
      AVX512_VBMI2: byte VPCOMPRESS, VPEXPAND  = false                                         
      AVX512_VNNI: neural network instructions = false                                                                                                                                         
      AVX512_BITALG: bit count/shiffle         = false                                         
      AVX512: VPOPCNTDQ instruction            = false              
      AVX512_4VNNIW: neural network instrs     = false                       
      AVX512_4FMAPS: multiply acc single prec  = false                                         
      AVX512_VP2INTERSECT: intersect mask regs = false           
      AVX512_FP16: fp16 support                = false          
         AVX state                            = false                      
         AVX-512 opmask                       = false                                          
         AVX-512 ZMM_Hi256                    = false                                          
         AVX-512 Hi16_ZMM                     = false 
```
</details>
 



cc: @stanciuadrian
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `b2ed1b72fa56e71d53af213e6e5557dcce171a2c` and the full history behind it is present.
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
