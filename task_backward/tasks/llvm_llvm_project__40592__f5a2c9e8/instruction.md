# Locate the commit that introduced this regression

A regression was reported against `llvm/llvm-project`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Assertion failure in defaultedDestructorIsDeleted

|  |  |
| --- | --- |
| Bugzilla Link | [41247](https://llvm.org/bz41247) |
| Resolution | FIXED |
| Resolved on | Mar 28, 2019 07:32 |
| Version | trunk |
| OS | Linux |
| CC | @AnastasiaStulova,@riccibruno |

## Extended Description 
$ cat t-86050e.cpp 
# 1 "<built-in>"
# 1 "t.cpp"
struct A {
        ~A() { }
};
struct B: A {
        B(): A() { }
        virtual ~B() // Expect missing ';' error message
private:
        void C() { }
};
int main() {
        B b;
        return 0;
}

$ clang -c t.cpp
t.cpp:8:2: error: expected '(' or '{'
        void C() { }
        ^
clang-9: .../llvm-project/clang/include/clang/AST/DeclCXX.h:931: bool clang::CXXRecordDecl::defaultedDestructorIsDeleted() const: Assertion `(!needsOverloadResolutionForDestructor() || (data().DeclaredSpecialMembers & SMF_Destructor)) && "this property has not yet been computed by Sema"' failed.

git bisect pointing to
```

## What you have

- `/testbed/repo` is a git clone of `llvm/llvm-project` truncated just after the regression was
  reported.  `HEAD` is `982726ea010fda10ecb87a851ed08a2df740c05b` and the full history behind it is present.
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
