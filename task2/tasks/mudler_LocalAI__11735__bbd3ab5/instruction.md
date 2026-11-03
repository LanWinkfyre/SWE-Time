# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
SIGSEGV at startup on Apple M5: go-m1cpu v0.1.6 (via gopsutil/v3) NULL-derefs an IORegistry property in package init(), killing every command including `--version`

**LocalAI version:**

`v4.9.0` (current release). The offending dependency pin is present in every tagged release I checked back to `v2.20.0`, so this is not a regression introduced by v4.9.0.

Reproduced with both:
- the Homebrew formula `localai` (bottle `arm64_tahoe`), and
- the official `darwin-arm64` binary from GitHub Releases.

Both are affected because the cause is a version pin in `go.mod`, not a packaging detail.

**Environment, CPU architecture, OS, and Version:**

- Apple **M5 Pro**, macOS **26.5.2**, arm64
- Works correctly on Apple **M4 Pro** / macOS 15.7.7 with the identical binary version — the failure is specific to M5

**Describe the bug**

On Apple M5, `local-ai` dies with `SIGSEGV` before it does any work. The crash happens in a package `init()` during cgo execution, so it is not tied to any subcommand, model, or backend: **every** invocation dies, including `local-ai --version`. There is no usable output and no way to configure around it.

**To Reproduce**

On an Apple M5 machine:

```
local-ai --version
```

**Logs**

```
SIGSEGV: segmentation violation
PC=0x18ca2978c m=0 sigcode=2 addr=0x0
signal arrived during cgo execution

goroutine 1 gp=0x2244fc6f41e0 m=0 mp=0x10bbbe460 [syscall, locked to thread]:
runtime.cgocall(0x1059cc35c, 0x2244fc7d0e08)
        /opt/homebrew/Cellar/go/1.26.7/libexec/src/runtime/cgocall.go:167 +0x44
github.com/shoenig/go-m1cpu._Cfunc_initialize()
        _cgo_gotypes.go:138 +0x2c
github.com/shoenig/go-m1cpu.init.0()
        .../github.com/shoenig/go-m1cpu@v0.1.6/cpu.go:148 +0x1c
runtime.doInit1(0x10b30e130)
```

**Root cause**

`github.com/shoenig/go-m1cpu v0.1.6` is pinned in `go.mod` as an indirect dependency. It reaches the binary through `github.com/shirou/gopsutil/v3 v3.24.5`:

```
cmd/local-ai
  -> core/services/monitoring, core/schema, pkg/xsysinfo
    -> github.com/shirou/gopsutil/v3/process, .../disk
      -> github.com/shirou/gopsutil/v3/cpu   (darwin)
        -> github.com/shoenig/go-m1cpu
```

`gopsutil/v3/cpu/cpu_darwin.go` calls `m1cpu.IsAppleSilicon()` / `m1cpu.PCoreHz()`, which is enough to link the package — and in v0.1.6 the cgo initialiser runs unconditionally from `init()`:

```go
func init() {
	C.initialize()
}
```

`initialize()` walks the IORegistry looking for the `pmgr` node and reads two properties:

```c
CFTypeRef pCoreRef = IORegistryEntryCreateCFProperty(obj, CFSTR("voltage-states5-sram"), kCFAllocatorDefault, 0);
CFTypeRef eCoreRef = IORegistryEntryCreateCFProperty(obj, CFSTR("voltage-states1-sram"), kCFAllocatorDefault, 0);

long long pCoreHz = getFrequency(pCoreRef);
```

and `getFrequency` in v0.1.6 dereferences the result without checking it:

```c
UInt64 getFrequency(CFTypeRef typeRef) {
  CFDataRef cfData = typeRef;
  CFIndex size = CFDataGetLength(cfData);   // <-- NULL deref when the property is absent
```

On M5 those properties are not exposed in the shape v0.1.6 expects, so `IORegistryEntryCreateCFProperty` returns `NULL` and `CFDataGetLength(NULL)` faults — matching the `addr=0x0` / `signal arrived during cgo execution` in the trace above.

Upstream fixed exactly this. `go-m1cpu v0.2.2` adds the missing guard:

```c
UInt64 getFrequency(CFTypeRef typeRef) {
  if (typeRef == NULL) {
    return 0;
  }
  CFDataRef cfData = typeRef;
```

and, just as importantly for the blast radius here, it **removes the `init()` entirely** in favour of a lazy `sync.Once`, so the IORegistry probe no longer runs at process start:

```go
var initOnce sync.Once

func ensureInitialized() {
	initOnce.Do(func() {
		C.initialize()
	})
}
```

v0.2.2 also releases the CF objects it creates (`CFRelease` / `IOObjectRelease`), which v0.1.6 leaks.

**Impact**

Any user on Apple M5 hardware, using any LocalAI release that pins `go-m1cpu v0.1.6`, cannot start LocalAI at all — not the API server, not the CLI, not `--version`. Since Apple Silicon Macs are a first-class target for the Metal backends, this effectively blocks the whole platform on current-generation hardware.

**Proposed fix**

Bump the indirect pin to `github.com/shoenig/go-m1cpu v0.2.2`. The exported Go API is unchanged between v0.1.6 and v0.2.2 (`IsAppleSilicon`, `PCoreHz`, … all keep their signatures), and the non-darwin stub file is byte-identical, so `gopsutil/v3` compiles against it untouched and no other platform is affected.

Note that bumping `gopsutil/v3` itself is not an option: `v3.24.5` is the final v3 release, so the v3 line will never carry this fix. Migrating to `gopsutil/v4` (which no longer depends on `go-m1cpu` at all, and is already in this module graph as an indirect dependency) would be the longer-term cleanup, but it is a bigger, behaviour-affecting change than a crash fix should carry.

I have a PR ready with the one-line bump.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `bbd3ab5a1458498895fa142b633579ad3436471b`.  There
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
{"case_id": "mudler_LocalAI__11735__bbd3ab5",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
