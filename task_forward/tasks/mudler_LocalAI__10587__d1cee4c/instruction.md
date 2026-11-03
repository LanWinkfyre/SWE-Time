# Recover the symbolic verification state this change produces

A regression report was filed against `mudler/LocalAI`.  The report is quoted verbatim below.

## Report

```
Import derives model name from URI repo root instead of selected GGUF file when URI lacks a file component

**LocalAI version:**
v4.5.5, source code analysis for mudler/LocalAI@d1cee4c52aebb54d291488e457f218bbdede2e1c

**Environment, CPU architecture, OS, and Version:**
Linux miki-linux-ai 7.1.2-2-cachyos #1 SMP PREEMPT_DYNAMIC Sun, 28 Jun 2026 15:38:15 +0000 x86_64 GNU/Linux
CPU: AMD Ryzen 9950X3D
OS: CachyOS, rolling release

**Describe the bug**
When importing a HuggingFace GGUF model via the Web UI, if the user enters a URI that points to a repository root without a specific file (e.g. `hf://owner/repo` or `huggingface://owner/repo`) and leaves the "Model Name" field empty, the importer uses the **repository name** (the last path component of the URI) as the model name — not the name of the individual GGUF file the importer would select from the repository's file listing.

This happens even when the user explicitly picks a specific GGUF file from the repository's available files. The gallery entry files are correctly grouped into shards, but the `model:` field in the emitted YAML configuration and the gallery entry `Filename` both derive from `filepath.Base(details.URI)`, which for a repo-root URI is the repo name, not the file name.

**To Reproduce**
1. In the Web UI, navigate to "Import New Model"
2. Set Mode to "Advanced" (Power mode)
3. In the Model URI field, enter `hf://TheBloke/Llama-2-7B-Chat-GGUF` (no filename)
4. Leave the "Model Name" field empty
5. Click "Import Model"
6. Observe that the resulting YAML configuration has `model:` set to `Llama-2-7B-Chat-GGUF` instead of the actual filename of the GGUF file selected from the repository

**Expected behavior**
The model name should be the name (minus extension) of the specific GGUF file for the primary (non-MMProj, non-MTP) model file selected from the repository. This corresponds to what the help text in the input box for the model name suggests.. The importer iterates `details.HuggingFace.Files` to find and group shard files, but the emitted YAML's `model:` field and gallery `Filename` should derive from the actual selected file, not `filepath.Base(details.URI)`.

**Additional context**
The relevant code is in `core/gallery/importers/llama-cpp.go`, `LlamaCPPImporter.Import()`:

```go
name, ok := preferencesMap["name"].(string)
if !ok {
    name = filepath.Base(details.URI)
}
```

When the URI is `hf://owner/repo` (no file component), `filepath.Base()` returns the repository name. The HF branch then correctly scans and groups files in `details.HuggingFace.Files`, but the `name` variable used for the gallery entry path prefix and the YAML `model:` field is the repo name, not the actual file name.

The same issue would affect any importer that matches a repo-root URI without a file component (e.g. `llama-cpp`, `mlx`, `transformers`, etc.) — all of them use `filepath.Base(details.URI)` as the fallback name.

**Related code paths**
- `core/gallery/importers/llama-cpp.go` — `Import()` function, lines ~85-170
- `core/gallery/importers/importers.go` — `DiscoverModelConfig()` function
- `pkg/downloader/uri.go` — `ResolveURL()` for HuggingFace URIs
- `core/http/endpoints/localai/import_model.go` — `ImportModelURIEndpoint()`
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d1cee4c52aebb54d291488e457f218bbdede2e1c`.  There
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
{"case_id": "mudler_LocalAI__10587__d1cee4c",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
