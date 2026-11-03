# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
WRONG code: likely instcombine of multiple i1:s.

This program should print 0:

```c
int printf(const char *, ...);
long a = 0, d = -1L, h = 0;
char b = 0, c = 0;
unsigned char g = 0;
int ****e = 0;
int *****f = &e;
int main() {
  long i = 0;
  for (g = 4; g; g++) {
    c = 0 >= a;
     //  -1      int64_max                        1          0 
    i = d > (9223372036854775807 - c) ? : (d + c);
    if (i) {
      char *j = &b;
      //  0                      int64_max         -1
      h = a > 9223372036854775807 - d; // OF 
      *j = h;
      *f = 0;
    }
  }
  printf("%d\n", b);
}
```

I think this program is well defined, as `i` will always be 0, and the overflowing subtract in the inner clause will never happen. 

```console
$ clang -O0 -march=z13 wrong0.i -o a.out ; ./a.out
0
$ clang -O1 -march=z13 wrong0.i -o a.out ; ./a.out
1
```

I have found this transformation by InstCombine which I think look suspicious:

```ll
for.body:                                         ; preds = %for.cond  
  %1 = load i64, ptr @a, align 8, !tbaa !7
  %cmp = icmp sge i64 0, %1
  %C = zext i1 %cmp to i32
  %D = load i64, ptr @d, align 8, !tbaa !7
  %MAX_min_C = sub nuw nsw i64 9223372036854775807, %C
  %CC_DGT = icmp sgt i64 %D, %MAX_min_C
  %BOOL_DGT = zext i32 %CC_DGT to i64
  %add = add nsw i64 %D, %C
  %cond = select i1 %CC_DGT, i64 %BOOL_DGT, i64 %add
  %tobool7 = icmp ne i64 %cond, 0
  br i1 %tobool7, label %enter, label %for.inc

*** IR Dump After InstCombinePass on main ***

for.body:                                         ; preds = %for.cond  
  %A = load i64, ptr @a, align 8, !tbaa !7
  %C_CC = icmp slt i64 %A, 1
  %D = load i64, ptr @d, align 8, !tbaa !7
  %C_BOOL = sext i1 %C_CC to i64
  %D_NE_MAX = icmp ne i64 %D, 9223372036854775807
  %NOT_C = xor i1 %C_CC, true
  %NOT_C_or_D_NE_MAX = select i1 %NOT_C, i1 true, i1 %D_NE_MAX
  %D_EQ_C = icmp eq i64 %D, %C_BOOL
  %tobool = select i1 %NOT_C_or_D_NE_MAX, i1 %D_EQ_C, i1 false
  br i1 %tobool, label %for.inc, label %enter
```

Before instcombine, it all makes sense, but then it seems that something has gone wrong: `%tobool` will be false (`d` is not equal to `c`), and as the branch targets have been swapped, the inner clause will now be entered, which is wrong.
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `e65cd4ce832b52d7b625a1e01cbecb264f9d2716` and the full history behind it is present.
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
