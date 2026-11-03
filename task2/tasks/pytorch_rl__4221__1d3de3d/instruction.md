# Recover the symbolic verification state this change produces

A regression report was filed against `pytorch/rl`.  The report is quoted verbatim below.

## Report

```
[BUG] History.from_text round-trip test never asserts role/content

## Describe the bug

`History.from_text` round-trip coverage in `test/llm/test_data.py` is effectively dead. `TestHistory.test_history_round_trip` is supposed to check that `History -> apply_chat_template -> History.from_text` recovers the original roles and contents (whitespace-normalized). The role/content assertions never run, so a broken inverse parser still passes CI.

This is a **test bug**, not a request to change `History`.

## To Reproduce

The live test is `TestHistory.test_history_round_trip` in `test/llm/test_data.py` (starts at line 840). After the round-trip parse:

```884:899:test/llm/test_data.py
        def norm(x):
            if isinstance(x, list):
                return [re.sub(r"\\s+", " ", str(xx).strip()) for xx in x]
            return re.sub(r"\\s+", " ", str(x).strip())
            # Compare roles and content
            assert norm(parsed.role) == norm(
                history.role
            ), f"Roles do not match!\nOriginal: {history.role}\nParsed: {parsed.role}"
            assert norm(parsed.content) == norm(
                history.content
            ), f"Content does not match!\nOriginal: {history.content}\nParsed: {parsed.content}"

        # All messages should be complete
        assert all(
            parsed.is_complete
        ), f"All messages should be complete after round-trip. is_complete: {parsed.is_complete}"
```

Two independent problems:

1. **Dead asserts.** `norm()` returns immediately after `re.sub` (line 887). The role/content `assert`s on lines 889-894 sit after that `return`, so they are unreachable. `norm()` is never even called from the test body.
2. **Wrong regex.** `r"\\s+"` is a raw string that matches a literal backslash-s (`\s+`), not whitespace. Even if the asserts were moved out of the function, whitespace normalization would not happen. The same regex is copied into `test_history_round_trip_incomplete` at lines 965-968.

The only assertion that actually executes in `test_history_round_trip` is `assert all(parsed.is_complete)` (lines 897-899). Completeness of messages does not check that the parser recovered the right roles or contents.

A chat-template inverse parser that returned any complete `History` of the right length (or even a single complete dummy message, depending on `is_complete` broadcasting) would still pass this test.

## Expected behavior

After `History.from_text` of a string produced by `apply_chat_template`, the recovered roles and contents should match the original history, compared after real whitespace normalization (`re.sub(r"\s+", " ", ...)`). That is what the comments next to the dead asserts already describe.

`test_history_round_trip_incomplete` should use the same (fixed) normalizer if it keeps comparing roles.

Please un-indent / move the asserts out of `norm()`, fix the regex, and keep this as a test-only change.

## Screenshots

N/A

## System info

Observed on a source checkout of pytorch/rl at `1d3de3db`.

```python
# test/llm/test_data.py, TestHistory.test_history_round_trip
```

## Additional context

`test_history_round_trip_incomplete` (line 916) has the same broken `r"\\s+"` pattern, but its role asserts sit *outside* `norm()` so they do run. They still do not normalize whitespace as intended.

## Reason and Possible fixes

Move the two asserts out of `norm()` so they execute, and change `r"\\s+"` to `r"\s+"`. No `History` API change is needed.

## Checklist

- [x] I have checked that there is no similar issue in the repo (**required**)
- [x] I have read the [documentation](https://github.com/pytorch/rl/tree/main/docs/) (**required**)
- [x] I have provided a minimal working example to reproduce the bug (**required**)
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `1d3de3dbd416877c02b2f44fe66a615fe55fb8e9`.  There
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
{"case_id": "pytorch_rl__4221__1d3de3d",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
