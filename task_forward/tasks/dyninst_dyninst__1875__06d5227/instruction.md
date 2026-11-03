# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
Add recognition of AMD MI300A GPU type

**Intention**
Use Dyninst to analyze binaries on an MI300A

**Describe the bug**
Dyninst doesn't recognize the architecture type

**To Reproduce**
I discovered this issue working in LLNL's restricted zone. I should be able to update this issue with a binary from Oregon's MI300A system.

**Expected behavior**
Dyninst should not abort when presented an AMD GPU binary for MI300A.

With the patch below, dyninst seems to work fine on MI300A - analyzing binaries and returning information as we expect.

**System (please complete the following information):**
 -  x86_64
 - master


**Additional context**
Here is a patch that fixes the issue:

```
diff --git a/dwarf/src/dwarfHandle.C b/dwarf/src/dwarfHandle.C
index c5e7a7d27..913e5e5cd 100644
--- a/dwarf/src/dwarfHandle.C
+++ b/dwarf/src/dwarfHandle.C
@@ -203,6 +203,7 @@ bool DwarfHandle::init_dbg()
         case EM_AMDGPU: { // TODO: This part of logic needs to be updated to reflect the table on the llvm website
             unsigned int ef_amdgpu_mach = 0x000000ff & file->e_flags();
             switch(ef_amdgpu_mach){
+                case 0x4c:
                 case 0x40:
                     arch = Dyninst::Arch_amdgpu_gfx940;
                     break;
diff --git a/elf/src/Elf_X.C b/elf/src/Elf_X.C
index 57ebd0a6d..bf4494958 100644
--- a/elf/src/Elf_X.C
+++ b/elf/src/Elf_X.C
@@ -1852,6 +1852,7 @@ Dyninst::Architecture Elf_X::getArch() const
                 //cerr << " dealing with amd gpu , mach = "  << std::hex << ef_amdgpu_mach << endl;
                 switch(ef_amdgpu_mach){
                     case 0x40:
+                    case 0x4c:
                         return Dyninst::Arch_amdgpu_gfx940;
                     case 0x3f:
                         return Dyninst::Arch_amdgpu_gfx90a;


```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `06d52274442016b997e59293d02848be08d7d94a`.  There
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
{"case_id": "dyninst_dyninst__1875__06d5227",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
