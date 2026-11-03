# Recover the symbolic verification state this change produces

A regression report was filed against `fallow-rs/fallow`.  The report is quoted verbatim below.

## Report

```
health: panic "byte index N is not a char boundary" on a quoted attribute with a backslash before a multi-byte char

### What happened?

`fallow health` panics when a quoted attribute value has a backslash immediately followed by a multi-byte character:

```
thread '<unnamed>' panicked at crates/extract/src/template_complexity.rs:607:34: byte index 7969 is not a char boundary; it is inside '\u{200b}' (bytes 7968..7971) of `<!DOCTYPE html>...`
```

`skip_quoted` (`template_complexity.rs:605`) advances a fixed 2 bytes past a backslash:

```rust
b'\\' => offset = (offset + 2).min(source.len()),
```

That assumes a single-byte escapee. With a multi-byte one (here U+200B, a 3-byte zero-width space) `offset` lands mid-character, and the next `source[offset..]` slice panics. Every other arm advances by `char::len_utf8`; this is the only one that doesn't.

Related (not a crash):

`sfc_template/angular.rs:370` and `:581` use the same `i += 2` escape advance. They don't panic (they only byte-index and slice at ASCII delimiters), but carry the same anti-pattern. Flagging for consistency.

### Reproduction

```rust
// "<a title='x\<U+200B>y' [class.x]='a && b' />"
compute_angular_template_complexity("<a title='x\\\u{200b}y' [class.x]='a && b' />");
// panics: byte index 13 is not a char boundary; it is inside '\u{200b}'
```

Or run `fallow health` over any tree with an HTML/template file whose quoted attribute contains `\` before a multi-byte char (saved/scraped HTML often embeds zero-width spaces).

### Expected behavior

Skip the escape and return normally — advance past the backslash, then one full char:

```rust
b'\\' => {
    offset += 1;
    if offset < source.len() {
        offset += source[offset..].chars().next().map_or(0, char::len_utf8);
    }
}
```

### Fallow version

2.9.2

### Operating system

macOS

### Configuration

```toml

```
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `d04815b71bc795ed1c59fb45c031962600030934`.  There
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
{"case_id": "fallow_rs_fallow__1201__d04815b",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
