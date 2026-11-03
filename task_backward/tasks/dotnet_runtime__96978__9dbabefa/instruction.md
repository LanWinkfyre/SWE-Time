# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
[RISC-V] Optimizing assemblies for size failed

### Description

On 8.0 release runtime can be built with the following command without any issues:
```
cd runtime
./build.sh --ci -c Release --cross --arch riscv64
```
However there is an error on the upcoming 9.x:
```
error NETSDK1144: Optimizing assemblies for size failed. Optimization can be disabled by setting the PublishTrimmed property to false. [/__w/dotnet_riscv/dotnet_riscv/runtime/src/coreclr/tools/aot/crossgen2/crossgen2_publish.csproj]
```

 Sorry, not an expect of Dotnet and I don't know the relationship between Mono and Crossgen2, but this might be a kind of regression.

### Reproduction Steps

```
./build.sh --ci -c Release --cross --arch riscv64
```

### Expected behavior

successful build process

### Actual behavior

error NETSDK1144

### Regression?

_No response_

### Known Workarounds

workaround by patching [eng/Subsets.props](https://github.com/dotnet/runtime/blob/main/eng/Subsets.props), but that doesn’t seem correct.
```patch
--- a/eng/Subsets.props
+++ b/eng/Subsets.props
@@ -29,6 +29,7 @@
     <DefaultPrimaryRuntimeFlavor>CoreCLR</DefaultPrimaryRuntimeFlavor>
     <DefaultPrimaryRuntimeFlavor Condition="'$(TargetArchitecture)' == 'armv6'">Mono</DefaultPrimaryRuntimeFlavor>
     <DefaultPrimaryRuntimeFlavor Condition="'$(TargetArchitecture)' == 'ppc64le'">Mono</DefaultPrimaryRuntimeFlavor>
+    <DefaultPrimaryRuntimeFlavor Condition="'$(TargetArchitecture)' == 'riscv64'">Mono</DefaultPrimaryRuntimeFlavor>
     <DefaultPrimaryRuntimeFlavor Condition="'$(TargetArchitecture)' == 's390x'">Mono</DefaultPrimaryRuntimeFlavor>
     <DefaultPrimaryRuntimeFlavor Condition="'$(TargetsLinuxBionic)' == 'true'">Mono</DefaultPrimaryRuntimeFlavor>
     <DefaultPrimaryRuntimeFlavor Condition="'$(TargetsMobile)' == 'true'">Mono</DefaultPrimaryRuntimeFlavor>
```

### Configuration

Docker image: `mcr.microsoft.com/dotnet-buildtools/prereqs:ubuntu-22.04-cross-riscv64`
`export ROOTFS_DIR=/crossrootfs/riscv64`

### Other information

_No response_



/cc @jkoritzinsky
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `6f9d6569684cc17015aa6fc5f9d9a5f7580ade97` and the full history behind it is present.
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
