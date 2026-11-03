# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
Windows: diagnostics fail to render — LSP emits \\?\ verbatim paths → [UriError] in asDiagnostics

### What happened?

On Windows, analysis runs to completion but no diagnostics render. The diagnostic queue throws [UriError] once per finding, because file locations from the LSP carry the Windows extended-length (\\?\) path prefix, which produces an illegal file:// URI (path begins with //, no authority component).

Smoking gun

The extension logs the workspace root with a \\?\ prefix that git's toplevel doesn't have — they are the same directory:


[warning] fallow workspace root (\\?\C:\Repositories\Personal\recipes) is a subdirectory
of git toplevel (C:\Repositories\Personal\recipes). Diagnostics for files outside the
workspace are not produced; the changedSince filter joins paths against the toplevel.
std::fs::canonicalize() on Windows always returns the \\?\ verbatim form. When those paths reach the VS Code client and are converted to a Uri, \\?\C:\… becomes file:////… and fails.

Error (repeats once per finding)


[error] Processing diagnostic queue failed.
Error: [UriError]: If a URI does not contain an authority component, then the path
cannot begin with two slash characters ("//")
    at i.parse (…/extensionHostProcess.js)
    at Object.b [as asUri]      (…/fallow-vscode-3.5.1/dist/extension.js:8:80654)
    at Object.S [as asDiagnostics] (…/fallow-vscode-3.5.1/dist/extension.js:8:81143)
    at e.LanguageClient.workDiagnosticQueue (…/fallow-vscode-3.5.1/dist/extension.js:10:10636)
Impact

Analysis itself succeeds (clone detection, dead-code scan of 96 components, plugin detection, and cache all complete in the log) — only the diagnostic-to-editor conversion breaks, so the Problems panel stays empty and the log fills with errors.

Expected

Strip the \\?\ verbatim prefix (or normalize via Uri.file() rather than Uri.parse()) before constructing diagnostic URIs, and normalize the workspace root so it isn't mistaken for a subdirectory of the git toplevel.

Steps to reproduce

Open any Git repo in VS Code on Windows.
Let Fallow run workspace analysis.
Observe the [UriError] flood in the Fallow output channel; no diagnostics appear.
Workarounds tried

No fallow.* setting controls path canonicalization (fallow.workspace is monorepo scoping only), so there's no user-side mitigation.

### Reproduction

Environment

Extension: fallow-rs.fallow-vscode v3.5.1
fallow-lsp.exe: auto-downloaded binary (globalStorage/fallow-rs.fallow-vscode/bin/fallow-lsp.exe)
OS: Windows 11 Pro (10.0.26200)
VS Code: <fill in — Help → About> (build 5264f2156c)

### Expected behavior

_No response_

### Fallow version

fallow-lsp 3.5.1

### Operating system

Windows

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `3ab6c16927f569c2df9455d0c393c5f66baf8b88`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "fallow_rs_fallow__1899__3ab6c16",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
