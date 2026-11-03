# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Read from invalid IncludeInfo object (version 1.9.2, Ubuntu 20.04)

**Describe the bug**
Segmentation fault in addIncludedUsingDirectives 

**Expected behavior**
No segmentation fault

**Screenshots**
Not appliciable

**To Reproduce**
Turn on USE_MATHJAX. Any variant appears to trigger the bug. The file it is processing when the fault happens:

https://github.com/milasudril/fruit/blob/fc256a0f0c447a16858069cb9cceefbba6d045e2/lib/event_handler.hpp

Clang assisted parsing was turned off, since I did not manage to compile it due to some problems with llvm packages.

**Version**
1.9.2 

**Stack trace**
```
Program received signal SIGSEGV, Segmentation fault.
FileDefImpl::addIncludedUsingDirectives (this=0x555556b1d170, visitedFiles=std::set with 14 elements = {...})
    at /dev/shm/doxygen-1.9.2/src/filedef.cpp:1423
1423              ii.fileDef()->addIncludedUsingDirectives(visitedFiles);
(gdb) bt
#0  FileDefImpl::addIncludedUsingDirectives (this=0x555556b1d170, visitedFiles=std::set with 14 elements = {...})
    at /dev/shm/doxygen-1.9.2/src/filedef.cpp:1423
#1  0x00005555557a97e8 in FileDefImpl::addIncludedUsingDirectives (this=0x555556b18090, 
    visitedFiles=std::set with 14 elements = {...}) at /dev/shm/doxygen-1.9.2/src/filedef.cpp:1423
#2  0x00005555556cc41f in findIncludedUsingDirectives () at /dev/shm/doxygen-1.9.2/src/doxygen.cpp:2179
#3  0x0000555555708629 in parseInput () at /dev/shm/doxygen-1.9.2/src/doxygen.cpp:11587
#4  0x00005555556c05b1 in main (argc=1, argv=0x7fffffffdff8) at /dev/shm/doxygen-1.9.2/src/main.cpp:37
(gdb) print m_includeList
$1 = {<std::vector<IncludeInfo, std::allocator<IncludeInfo> >> = std::vector of length 2, capacity 2 = {{
      m_fileDef = 0xc, includeName = {m_rep = "type_traits"}, local = false, imported = false}, {m_fileDef = 0x0, 
      includeName = {m_rep = "string"}, local = false, imported = false}}, <No data fields>}
 ```

**Additional context**
As you can see from my gdb session, I have modified IncludeInfo so I could get some logs:

```c++
/** Class representing the data associated with a \#include statement. */
struct IncludeInfo
{
  IncludeInfo() {
	  printf("Ctor %p\n", (void*)this);
}

  IncludeInfo(FileDef *fd,const QCString &in,bool loc,bool imp)
    : m_fileDef(fd), includeName(in), local(loc), imported(imp) {
		printf("Ctor %p in %p\n", (void*)m_fileDef, (const void*)this);
	}

  FileDef* fileDef() const {
	  printf("Get filedef %p from %p\n", (void*)m_fileDef, (const void*)this);
	  fflush(stdout);
	  return m_fileDef;
  }

  void fileDef(FileDef& fd) {
	  m_fileDef = &fd;
 }

private:
  FileDef *m_fileDef = nullptr;
public:
  QCString includeName;
  bool local = false;
  bool imported = false;
};
```
Then, it is clear that it reads from a IncludeInfo that have never existed. See attached log
[log.txt](https://github.com/doxygen/doxygen/files/7025534/log.txt)

```
Get filedef 0xc from 0x55957ca51e60
```
To me, this looks like some kind of memory corruption, so I tried valgrind, but failed to reproduce the error. When running with valgrind, I see this warning:

```
/home/torbjorr/Dokument/fruit/lib/event_handler.hpp:25: warning: Detected potential recursive class relation between class fruit::EventHandler and base class fruit::EventHandler< Events... >!

/home/torbjorr/Dokument/fruit/lib/event_handler.hpp:25: warning: Detected potential recursive class relation between class fruit::EventHandler and base class EventHandler< Events... >!
```
which does not appear without valgrind. As a side note, I think this warning is expected, since Doxygen has no support for recursive inheritance.
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `0d28550e0d4f51b7f6296818d72d5c30543874ba` and the full history behind it is present.
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
