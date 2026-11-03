# Locate the commit that introduced this regression

A regression was reported against `rust-lang/rust`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
vec macro into_boxed codegen regression

This is a regression from stable 1.42.0 to the latest beta & nightly

found because of this: https://internals.rust-lang.org/t/more-efficient-boxed-slice-creation/12271

```rust
pub fn bar2(n: usize) -> Box<[u32]> {
    vec![0; n].into_boxed_slice()
}
```

I think the regression happened because of a missed optimization to inline `alloc::raw_vec::RawVec<T,A>::allocate_in::{{closure}}`, so it generates unnecessary panic handlers

[stable](https://rust.godbolt.org/z/uSaaEr)

```asm
alloc::raw_vec::RawVec<T,A>::allocate_in::{{closure}}:
        push    rax
        call    qword ptr [rip + alloc::raw_vec::capacity_overflow@GOTPCREL]
        ud2

example::bar2:
        push    r14
        push    rbx
        push    rax
        mov     ecx, 4
        mov     rax, rdi
        mul     rcx
        jo      .LBB1_5
        mov     rbx, rdi
        mov     r14, rax
        test    rax, rax
        je      .LBB1_4
        mov     esi, 4
        mov     rdi, r14
        call    qword ptr [rip + __rust_alloc_zeroed@GOTPCREL]
        test    rax, rax
        je      .LBB1_6
        mov     rcx, rax
.LBB1_4:
        mov     rax, rcx
        mov     rdx, rbx
        add     rsp, 8
        pop     rbx
        pop     r14
        ret
.LBB1_5:
        call    alloc::raw_vec::RawVec<T,A>::allocate_in::{{closure}}
        ud2
.LBB1_6:
        mov     esi, 4
        mov     rdi, r14
        call    qword ptr [rip + alloc::alloc::handle_alloc_error@GOTPCREL]
        ud2
```
[nightly](https://rust.godbolt.org/z/KkhBH_)



Bisected with git bisect
```

## What you have

- `/testbed/repo` is a git clone of `rust-lang/rust` truncated just after the regression was
  reported.  `HEAD` is `65b448273dd280401cd440a6740a7cd891525ba3` and the full history behind it is present.
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
