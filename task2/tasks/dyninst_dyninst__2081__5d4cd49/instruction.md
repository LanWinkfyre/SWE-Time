# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
Failing to write instrumented shared library

**Intention**
Instrument library functions using BPatch_callBefore and BPatch_callAfter

**Describe the bug**
Segmentation fault when writing with writeFile, after inserting the snippets.

**To Reproduce**
Made  a copy of the examples here:
https://github.com/jordialcaraz/examples/tree/master

Clone the repository
Build the examples
Go to codeCoverage folder:
And execute the modified example:
`./code_coverage -s lib_to_instrument/libtorch_python.so libtorch_python.so`

**Expected behavior**
I would expect if to build without crashing.

**System (please complete the following information):**
System: x86_64

Installed Dyninst with `spack install dyninst`

```
  spack find -v -d dyninst
  -- linux-ubuntu22.04-cascadelake / %c,cxx=gcc@11.4.0 ------------
  dyninst@13.0.0~ipo+openmp~stat_dysect~static build_system=cmake build_type=Release generator=make
      boost@1.89.0+atomic~charconv+chrono~clanglibcpp~cobalt+container~context~contract~conversion~coroutine+date_time~debug+exception~fiber+filesystem~graph~graph_parallel~icu~iostreams~json~locale~log~math~mpi~mqtt5+multithreaded~nowide~numpy~pic~program_options~python+random~regex~serialization+shared~signals2~singlethreaded~stacktrace+system~taggedlayout~test+thread+timer~type_erasure~url~versionedlayout~wave build_system=generic cxxstd=11 patches:=a440f96 visibility=hidden
      cmake@3.31.9~doc+ncurses+ownlibs~qtgui build_system=generic build_type=Release
          curl@8.15.0~gssapi~ldap~libidn2~librtmp~libssh~libssh2+nghttp2 build_system=autotools libs:=shared,static tls:=openssl
              nghttp2@1.67.1 build_system=autotools
              openssl@3.6.0~docs+shared build_system=generic certs=mozilla
                  ca-certificates-mozilla@2025-08-12 build_system=generic
              perl@5.42.0+cpanm+opcode+open+shared+threads build_system=generic
                  berkeley-db@18.1.40+cxx~docs+stl build_system=autotools patches:=26090f4,b231fcc
                  gdbm@1.25 build_system=autotools
                      readline@8.3 build_system=autotools patches:=21f0a03
          ncurses@6.5-20250705~symlinks+termlib abi=none build_system=autotools patches:=7a351bc
          zlib-ng@2.2.4+compat+new_strategies+opt+pic+shared build_system=autotools
      compiler-wrapper@1.0 build_system=generic
      elfutils@0.193~debuginfod+exeprefix+nls build_system=autotools
          bzip2@1.0.8~debug~pic+shared build_system=generic
              diffutils@3.12 build_system=autotools
          gettext@0.23.1+bzip2+curses+git~libunistring+libxml2+pic+shared+tar+xz build_system=autotools
              libxml2@2.13.5~http+pic~python+shared build_system=autotools
              tar@1.35 build_system=autotools zip=pigz
                  pigz@2.8 build_system=makefile
          libiconv@1.18 build_system=autotools libs:=shared,static
          m4@1.4.20+sigsegv build_system=autotools
              libsigsegv@2.14 build_system=autotools
          pkgconf@2.5.1 build_system=autotools
          xz@5.6.3~pic build_system=autotools libs:=shared,static
          zstd@1.5.7+programs build_system=makefile compression:=none libs:=shared,static
      gcc@11.4.0~binutils+bootstrap~graphite~nvptx~piclibs~profiled~strip build_system=autotools build_type=RelWithDebInfo languages:='c,c++,fortran'
      gcc-runtime@11.4.0 build_system=generic
      glibc@2.35 build_system=autotools
      gmake@4.4.1~guile build_system=generic
      intel-tbb@2022.3.0~ipo+shared+tm build_system=cmake build_type=Release cxxstd=default generator=make
          hwloc@2.12.2~cairo~cuda~gl~level_zero~libudev+libxml2~nvml~opencl+pci~rocm build_system=autotools libs:=shared,static
              libpciaccess@0.17 build_system=autotools
                  util-macros@1.20.1 build_system=autotools
      libiberty@2.41+pic build_system=autotools
  
```

**Additional context**
We want to instrument shared libraries that are installed with python -m pip install

Seems to only throw the segmentation fault due to line 218 of code_coverage.C
`
BPatchSnippetHandle* handle_b = mutateeAddressSpace->insertSnippet(exitTrace, *funcExit, BPatch_callAfter, BPatch_lastSnippet);`

The error is not shown if that line is removed, but I would like to instrument both.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `5d4cd492383f3825257ad1f8145e839fb5667c8a`.  There
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
{"case_id": "dyninst_dyninst__2081__5d4cd49",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
