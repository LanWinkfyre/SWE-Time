# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Infinite loop when parsing a simple header file

**Describe the bug**

When generating documentation, doxygen gets stuck on a specific file and the cpu usage goes to 100% (one core)
The console log stops at the line

`Generating docs for file include/Base35.h...`

It also happens when I run doxygen on this file alone, included in the example archive

**Expected behavior**

The generation should succeed

**Screenshots**

![doxygen](https://github.com/doxygen/doxygen/assets/33872633/b8b865c6-f73d-4afd-a8ea-ea26ae0c0feb)

**To Reproduce**

There is an attached archive with a directory, containing 2 files: include/Base35.h and Doxyfile
I enter the directory, call doxygen Doxyfile and it gets stuck on the Base35.h file

**Version**

Operating system: Kubuntu 23.04

Doxygen 1.9.4 (comes with (K)ubuntu 23.04)
Also happens on Doxygen 1.9.8 (built from source)
Does not happen on Doxygen 1.9.1 (comes with (K)ubuntu 22.04)

**Stack trace**

As I saw, frame #4 (MemberList::writeDocumentation) does not exit.
This is backtrace from doxygen-1.9.4, as I am using gdb, which can automatically download debug symbols.

```
0x00005555558e81cc in isId (c=66) at /usr/src/doxygen-1.9.4-4/src/util.h:173
Downloading source file /usr/src/doxygen-1.9.4-4/src/util.h
173       return c=='_' || c>=128 || c<0 || isalnum(c) || c=='$';
(gdb) bt
#0  0x00005555558e81cc in isId (c=66) at /usr/src/doxygen-1.9.4-4/src/util.h:173
#1  addTemplateNames (s=..., n=..., t=...) at /usr/src/doxygen-1.9.4-4/src/memberdef.cpp:807
#2  0x00005555558f8ae3 in writeDefArgumentList (ol=..., scope=scope@entry=0x555556840ce8, md=md@entry=0x55555685f068) at /usr/src/doxygen-1.9.4-4/src/memberdef.cpp:948
#3  0x00005555559094ac in MemberDefImpl::writeDocumentation (this=0x55555685f060, ml=<optimized out>, memCount=<optimized out>, memTotal=<optimized out>, ol=..., scName=..., container=0x555556843f28, inGroup=false,
showEnumValues=false, showInline=false) at /usr/src/doxygen-1.9.4-4/src/memberdef.cpp:3519
#4  0x0000555555917ec7 in MemberList::writeDocumentation (this=this@entry=0x555556847f30, ol=..., scopeName=..., container=container@entry=0x555556843f28, title=..., showEnumValues=showEnumValues@entry=false,
showInline=false) at /usr/src/doxygen-1.9.4-4/src/memberlist.cpp:711
#5  0x0000555555736502 in FileDefImpl::writeMemberDocumentation (this=this@entry=0x555556843f20, ol=..., lt=<optimized out>, title=...) at /usr/src/doxygen-1.9.4-4/src/filedef.cpp:1669
#6  0x000055555573eb62 in FileDefImpl::writeDocumentation (this=0x555556843f20, ol=...) at /usr/src/doxygen-1.9.4-4/src/filedef.cpp:949
#7  0x000055555570b4b6 in generateFileDocs () at /usr/src/doxygen-1.9.4-4/src/doxygen.cpp:8208
#8  0x000055555570e663 in generateOutput () at /usr/src/doxygen-1.9.4-4/src/doxygen.cpp:12499
#9  0x000055555568a072 in main (argc=2, argv=0x7fffffffdbe8) at /usr/src/doxygen-1.9.4-4/src/main.cpp:38
(gdb)
```

**Additional context**

[doxygenIssue.tar.gz](https://github.com/doxygen/doxygen/files/12507955/doxygenIssue.tar.gz)

This is an example containing the Doxyfile and the file from the project that reproduces the issue. I think that the files that it includes (Buffer.h and EncodeError.h) are not needed.


Nice small example and references to the different versions.




I looked in the code and saw the line:
```
inline namespace Rigel {
```
and when removing the `inline` we get:
```
namespace Rigel {
```
and doxygen runs, but this cannot be the real solution.


Bisecting gave that the problem is introduced between doxygen 1.9.1 and 1.9.2 and more precise:



@doxygen any idea?
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `d062df6c56464f8063acb4fceb989e0cffdd754a` and the full history behind it is present.
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
