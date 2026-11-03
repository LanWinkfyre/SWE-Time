# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Clang at -O2 produced the wrong code.



Compiler explorer: https://godbolt.org/z/rhfGPe4x5

```console
% cat a.c
int printf(const char *, ...);
long a, b, i;
char c, f;
int d;
short e;
int *g = &d;
unsigned h;
char j[1];
int main() {
  short *k = &e;
  for (; *g;)
    ;
  for (; c <= 30; c++) {
    if (b > 4)
      i = a;
    else
      i = b;
    (int)i + 6 || (*k = j != &f);
    *g ^= h;
  }
  printf("%d\n", e);
}
%
% clang a.c -O0 && ./a.out
0
% clang a.c -O2 && ./a.out
1
%
```
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `24e33b594503f0283d31b89e2694e3d798def5ac` and the full history behind it is present.
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
