# Locate the commit that introduced this regression

A regression was reported against `Comfy-Org/ComfyUI`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
### Custom Node Testing

- [ ] I have tried disabling custom nodes and the issue persists (see [how to disable custom nodes](https://docs.comfy.org/troubleshooting/custom-node-issues#step-1%3A-test-with-all-custom-nodes-disabled) if you need help)

### Expected Behavior

wan workflows to work as before.

### Actual Behavior

With the latest commit my wan workflows output noise. Before ksampler I also see log:

```
unet unexpected: ['scaled_fp8', 'text_embedding.0.scale_input', 'text_embedding.0.scale_weight', ...
```






### Steps to Reproduce

Run wan 2.2 workflow

### Debug Logs

```powershell
unet unexpected: ['scaled_fp8', 'text_embedding.0.scale_input', 'text_embedding.0.scale_weight', ...
```

### Other

_No response_
```

## What you have

- `/testbed/repo` is a git clone of `Comfy-Org/ComfyUI` truncated just after the regression was
  reported.  `HEAD` is `076639fed99742f43ffbf0b0df34bb8fd105b8e9` and the full history behind it is present.
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
