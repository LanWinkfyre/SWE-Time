# Locate the commit that introduced this regression

A regression was reported against `openssl/openssl`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
openssl 3.6 breaks the qatprovider

 
The failure:
```
openssl speed -provider qatprovider -seconds 1 -elapsed -elapsed rsa2048
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/x86_64-linux-gnu/libthread_db.so.1".

QAT_SW - Processor unsupported: AVX512F = 0, AVX2 = 0, VAES = 0, VPCLMULQDQ = 0
You have chosen to measure elapsed time instead of user CPU time.
Doing 2048 bits private rsa sign ops for 1s: 496 2048 bits private RSA sign ops in 1.00s
Doing 2048 bits public rsa verify ops for 1s: 16583 2048 bits public RSA verify ops in 1.00s
Doing 2048 bits public rsa encrypt ops for 1s: 15849 2048 bits public RSA encrypt ops in 1.00s
Doing 2048 bits private rsa decrypt ops for 1s: 488 2048 bits private RSA decrypt ops in 1.00s

Program received signal SIGSEGV, Segmentation fault.

___pthread_rwlock_rdlock (rwlock=rwlock@entry=0x0) at ./nptl/pthread_rwlock_rdlock.c:26
⚠️ warning: 26   ./nptl/pthread_rwlock_rdlock.c: No such file or directory
(gdb) bt
#0  ___pthread_rwlock_rdlock (rwlock=rwlock@entry=0x0) at ./nptl/pthread_rwlock_rdlock.c:26
#1  0x00007ffff7a3b809 in ossl_rwlock_rdlock (rwlock=rwlock@entry=0x0) at ../crypto/threads_pthread.c:885
#2  CRYPTO_THREAD_read_lock (lock=lock@entry=0x0) at ../crypto/threads_pthread.c:950
#3  0x00007ffff793bc7c in BN_MONT_CTX_set_locked (pmont=pmont@entry=0x5555557159e8, lock=0x0, mod=0x555555714fe0, ctx=ctx@entry=0x555555714e60) at ../crypto/bn/bn_mont.c:431
#4  0x00007ffff7b2e492 in rsa_ossl_public_encrypt (flen=256,
    from=0x555555716380,
    to=0x555555716270 , rsa=0x555555715940, padding=3) at ../crypto/rsa/rsa_ossl.c:197
#5  0x00007ffff7bf829e in rsasve_generate (prsactx=0x55555570a1e0, out=0x555555716270 "\2264$", outlen=0x7fffffffd928,
    secret=0x555555716380 ,    secretlen=0x7fffffffd920) at providers/implementations/kem/rsa_kem.c:423
#6  rsakem_generate (vprsactx=0x55555570a1e0, out=0x555555716270 "\2264$", outlen=0x7fffffffd928,
    secret=0x555555716380,  secretlen=0x7fffffffd920) at providers/implementations/kem/rsa_kem.c:512
#7  rsakem_generate (vprsactx=0x55555570a1e0, out=0x555555716270 "\2264$", outlen=0x7fffffffd928,
    secret=0x555555716380 ,  secretlen=0x7fffffffd920) at providers/implementations/kem/rsa_kem.c:502
#8  0x00005555555f15d8 in speed_main (argc=<optimized out>, argv=<optimized out>) at ../apps/speed.c:4210
#9  0x00005555555c61b2 in do_cmd (prog=prog@entry=0x555555680580, argc=argc@entry=8, argv=argv@entry=0x7fffffffde40) at ../apps/openssl.c:490
#10 0x000055555559bcf6 in main (argc=<optimized out>, argv=<optimized out>) at ../apps/openssl.c:366

```
The passed argument rsa_st::lock is NULL. Is this likely to be shortcoming on the  provider's side due missing initialize that part or is something in openssl that is missing this?

Sebastian
```

## What you have

- `/testbed/repo` is a git clone of `openssl/openssl` truncated just after the regression was
  reported.  `HEAD` is `40f076965f154e307a0821088b6adcc447ceae01` and the full history behind it is present.
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
