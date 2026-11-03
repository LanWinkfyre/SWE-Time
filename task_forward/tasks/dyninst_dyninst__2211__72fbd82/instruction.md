# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
[dyninstAPI] Performance degradation observed with commit cc547f688

**Intention**
I'm working with `rocprof-sys-instrument` and I'm experimenting with bumping up the commit hash in our dyninst submodule. When I bumped to head, I noticed a massive performance degradation. Using git bisect, I was able to learn that:
```
cc547f688  Extract arch-specific register clobbering out of parse_func (#2148)
```
Is the cause of (most of) our problems. Specifically, the root cause seems to be the refactored `writesFPRs` from cached member function to uncached free function. 

**Describe the bug**
Essentially, `proc->finalizeInsertSet(true, ...)` takes much longer in commit `cc547f688`. 
Using `rocprof-sys-instrument` and an openmp offload program (I have a simpler reproducer in the reproducer section):

```
# Problem commit cc547f688

# Run 1
[rocprof-sys][exe] [timing] finalize insertion set :: 53.465 sec

# Run 2
[rocprof-sys][exe] [timing] finalize insertion set :: 167.747 sec


# Parent commit 877171ee4

# Run 1
[rocprof-sys][exe] [timing] finalize insertion set :: 6.395 sec

# Run 2
[rocprof-sys][exe] [timing] finalize insertion set :: 5.542 sec
```

Reason seems that the caching was removed. Indeed, when I add to `inst-x86.C` within `bool writesFPRs(parse_func *func, unsigned level)` a simple storage mechanism:
```
[...]
  enum FPRState : uint8_t { unknown, used, unused };
  static std::unordered_map<parse_func*, FPRState> cache;

  if (level == 0) {
    auto it = cache.find(func);
    if (it != cache.end())
      return it->second == used;
  }
  if (level >= 3) {
    return true; // Arbitrarily decided level 3 iteration.
  }

  for (auto *e : func->callEdges()) {
    if (!e->trg())
      continue;
    auto *target = func->obj()->findFuncByEntry(func->region(), e->trg()->start());
    parse_func *ct = dynamic_cast<parse_func*>(target);
    if (ct) {
      if (writesFPRs(ct, level + 1)) {
        // One of our kids does... if we're top-level, cache it; in
        // any case, return
        if (level == 0)
          cache[func] = used;
        return true;
      }
    } else if (!ct) {
      // Indirect call... oh, yeah.
      if (level == 0)
        cache[func] = used;
      return true;
    }
  }

[...]
// And modify the for loop at the EOF

  for (auto *fe : func->extents()) {
    void *iptr = func->isrc()->getPtrToInstruction(fe->start());
    auto *buf = reinterpret_cast<const unsigned char *>(iptr);
    if (!buf) {
      parsing_printf("%s[%d]: failed to get insn ptr at %lx\n", FILE__,
                     __LINE__, fe->start());
      // if the function cannot be parsed, it is only safe to
      // assume that the FPRs are written -- mcnulty
      if (level == 0)
        cache[func] = used;
      return true;
    }

    InstructionDecoder d(buf, fe->end() - fe->start(), func->isrc()->getArch());
    Instruction i = d.decode();

    while (i.isValid()) {
      for (auto &r : candidate_regs) {
        if (i.isWritten(r)) {
          if (level == 0)
            cache[func] = used;
          return true;
        }
        i = d.decode();
      }
    }
  }
  if (level == 0)
    cache[func] = unused;
  return false;
}
```

I get massively improved performance:
```
# Problem commit, but with modifications above:

# Run 1
[rocprof-sys][exe] [timing] finalize insertion set :: 6.012 sec

# Run 2
[rocprof-sys][exe] [timing] finalize insertion set :: 7.692 sec
```

**Note**: I had tested this against head a few days ago and the same problem was still present. 

**To Reproduce**
Reproducing in `rocprof-sys-instrument` is not straightforward due to the submodule shenanigans that had to be done. Instead, consider the following simple reproducer. 

`target.c`
```
#include <omp.h>
#include <stdio.h>

int main() {
    omp_set_num_threads(2);
    printf("threads = %d\n", omp_get_max_threads());
    return 0;
}
```

And a custom `instrumenter.cpp`:
```
#include <BPatch.h>
#include <BPatch_function.h>
#include <BPatch_module.h>
#include <BPatch_point.h>
#include <BPatch_snippet.h>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <vector>

int main(int argc, char** argv) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <target>\n", argv[0]);
        return 1;
    }

    using clock = std::chrono::steady_clock;

    BPatch bpatch;
    bpatch.setTypeChecking(true);
    bpatch.setSaveFPR(true);
    bpatch.setInstrStackFrames(false);
    bpatch.setLivenessAnalysis(false);
    bpatch.setTrampRecursive(false);

    auto t0 = clock::now();
    BPatch_process* proc = bpatch.processCreate(argv[1], (const char**)&argv[1]);
    auto t1 = clock::now();
    printf("[timing] processCreate          : %.3f sec\n",
           std::chrono::duration<double>(t1 - t0).count());

    if (!proc) {
        fprintf(stderr, "Error: failed to create process for '%s'\n", argv[1]);
        return 1;
    }

    BPatch_image* image = proc->getImage();
    std::vector<BPatch_function*>* funcs = image->getProcedures();
    printf("[info]   %zu total procedures found\n", funcs->size());

    std::vector<BPatch_function*> call_target;
    image->findFunction("omp_get_thread_num", call_target);
    if (call_target.empty()) {
        fprintf(stderr, "Error: could not find 'omp_get_thread_num'\n");
        return 1;
    }
    std::vector<BPatch_snippet*> call_args;
    BPatch_funcCallExpr call_expr(*call_target[0], call_args);

    proc->beginInsertionSet();

    auto t2 = clock::now();
    size_t count = 0;
    for (auto* f : *funcs) {
        if (!f->isInstrumentable()) continue;

        BPatch_module* mod = f->getModule();
        if (!mod) continue;
        char modname[1024];
        mod->getName(modname, sizeof(modname));
        if (!strstr(modname, "libomptarget") && !strstr(modname, "libomp.so")) // Can remove libomp.so
            continue;

        // This causes finalizeInsertionSet performance to degrade
        auto* entries = f->findPoint(BPatch_entry); // Smaller time difference when only this
        auto* exits   = f->findPoint(BPatch_exit); // Larger time difference when both are added

        if (entries && !entries->empty()) {
            proc->insertSnippet(call_expr, *entries);
            count++;
        }
        if (exits && !exits->empty()) {
            proc->insertSnippet(call_expr, *exits);
        }
    }
    auto t3 = clock::now();
    printf("[timing] insertSnippet (%zu fns) : %.3f sec\n", count,
           std::chrono::duration<double>(t3 - t2).count());

    auto t4 = clock::now();
    bool modified = true;
    proc->finalizeInsertionSet(true, &modified);
    auto t5 = clock::now();
    printf("[timing] finalizeInsertionSet    : %.3f sec\n",
           std::chrono::duration<double>(t5 - t4).count());

    proc->detach(true);
    return 0;
}
```

Now suppose you build dyninst at the "problem" commit (cc547f688) and the "parent" commit (877171ee4):

```
# Build Dyninst at parent commit
cd /path/to/dyninst
git checkout 877171ee4
cmake -B build-parent -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$PWD/install-parent
cmake --build build-parent --parallel $(nproc)
cmake --install build-parent

# Build Dyninst at problem commit
git checkout cc547f688
cmake -B build-problem -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=$PWD/install-problem
cmake --build build-problem --parallel $(nproc)
cmake --install build-problem
```

Then build the instrumenter against these commits:

```
# Build instrumenter against parent
g++ -std=c++17 \
    -I/path/to/dyninst/install-parent/include \
    -L/path/to/dyninst/install-parent/lib \
    -o instrument-parent instrument.cpp \
    -ldyninstAPI -lcommon -linstructionAPI -lsymtabAPI -lparseAPI -lpatchAPI -lstackwalk -lpcontrol \
    -Wl,-rpath,/path/to/dyninst/install-parent/lib

# Build instrumenter against problem
g++ -std=c++17 \
    -I/path/to/dyninst/install-problem/include \
    -L/path/to/dyninst/install-problem/lib \
    -o instrument-problem instrument.cpp \
    -ldyninstAPI -lcommon -linstructionAPI -lsymtabAPI -lparseAPI -lpatchAPI -lstackwalk -lpcontrol \
    -Wl,-rpath,/path/to/dyninst/install-problem/lib
```

Now build `target.c` with offload support:
```
amdclang -fopenmp --offload-arch=native -o target target.c
```

We explicitly use `offload-arch` as that allows `libomptarget.so` (which contains many procedures to be instrumented). I believe you should be able to reproduce this with any program that contains a sufficient number of procedures. 

Then run the program:
```
# Run both and compare
./repro/instrument-parent ./repro/target
./repro/instrument-problem ./repro/target
```

We notice:
```
# PARENT
[timing] processCreate          : 5.583 sec
[info]   63501 total procedures found
[timing] insertSnippet (51183 fns) : 0.355 sec
[timing] finalizeInsertionSet    : 86.899 sec
threads = 2

# PROBLEM
[timing] processCreate          : 5.586 sec
[info]   63497 total procedures found
[timing] insertSnippet (51179 fns) : 0.352 sec
[timing] finalizeInsertionSet    : 130.309 sec
threads = 2
```
A 44 second difference...


**Expected behavior**
I expect it to not take so long. Indeed, with the change in `inst-x86.C` within `bool writesFPRs(parse_func *func, unsigned level)` that I've described above, results return to what I expect:

```
# PROBLEM commit BUT with changes
[timing] processCreate          : 5.500 sec
[info]   63497 total procedures found
[timing] insertSnippet (51179 fns) : 0.355 sec
[timing] finalizeInsertionSet    : 87.376 sec
threads = 2
```

**System (please complete the following information):**
 - What platform (x86, x86_64, Power8, Power9, ARMv8) `x86_64`
 - What commit? `"problem" commit (cc547f688) and the "parent" commit (877171ee4)`
 - Maybe libc version: `ldd (Ubuntu GLIBC 2.39-0ubuntu8.7) 2.39`
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `72fbd82bf4d19bf92c9f570563df2fb4ccce59ed`.  There
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
{"case_id": "dyninst_dyninst__2211__72fbd82",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
