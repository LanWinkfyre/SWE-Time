# Locate the commit that introduced this regression

A regression was reported against `PerryTS/perry`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
GC: `this` holds a stale from-space pointer after a moving collection inside a method body

`cargo test -p perry --test gc_property_key_operand_rooting_6935` fails 2 of 3 on `main`, under the forced-evacuation env the suite exists to exercise (`PERRY_GC_FORCE_EVACUATE=1`, `PERRY_GC_VERIFY_EVACUATION=1`):

```
proxy_target_set_survives_forced_evacuation ......... FAILED
property_key_stored_values_survive_forced_evacuation  FAILED
property_key_receivers_survive_forced_evacuation ....  ok
```

The compiled binaries exit 1 with values that came back missing across a collection:

```
FAIL proxy-forward-set.tag got=undefined want=30
TypeError: Cannot convert undefined or null to object

FAIL dyn-index-set payload missing
FAIL dyn-index-set-toprimitive payload missing
FAIL class-static-computed.tag got=undefined want=6
```

That is the unrooted-value-across-collection signature this suite was written for (#6935).



 Reproduces locally on macOS (no Linux needed).

**Reproduce:**
```
cargo build --profile perry-dev -p perry -p perry-runtime-static -p perry-stdlib-static
PERRY_RUNTIME_DIR=$PWD/target/perry-dev \
  cargo test --profile perry-dev -p perry --test gc_property_key_operand_rooting_6935
```

**Ruled out:**
- **Not the `-Os` default.** Re-running with `PERRY_LL_SIZE_OPT=0` (restoring `-O3`) fails identically. *Caveat*: that run finished in 4s versus 202s, which looks like object-cache reuse rather than a real recompile — worth re-confirming with a cleared `node_modules/.cache/perry` before treating the `-Os` arm as fully excluded.

- The object-cache key change in #8418 itself looks correct — it adds `PERRY_LL_SIZE_OPT` / `PERRY_LL_PREOPT_OPTNONE_INSTRS` to the hash.

The likeliest remaining suspects inside #8418 are the ~304-line `run_pipeline.rs` restructuring and the `collect_modules` / `json_module` split, rather than the opt-in `PERRY_LL_PREOPT_OPTNONE_INSTRS` path (default 0 = disabled).

 With that abort fixed, this is now the visible `cargo-test` failure, and `cargo-test` is required by `full-suite-gate`.




Endpoints, each confirmed by running the suite rather than assumed:

| commit | result |
|---|---|



| `origin/main` | 2 failed |

So the suite *did* work once — this is a real regression, not a test that never passed here — .

 

 

That is consistent with how long this went unwatched — `full-suite-gate` has been red since June and `cargo-test` stops at its first failing suite, so nothing has guarded this file for months and causes could accumulate silently.

**Suggested approach for whoever takes it** (iteration is cheap — the suite passes `--no-cache` and a run is ~5 s once warm):
1.  repeat until a revert of the identified set actually restores green.
2. Or attack it directly from the shape side, which may be faster: dump the anon-shape pointer mask for `payload(t)` (`{tag: number, arr: [...], s: string}`) , and check whether `arr`/`s` are being marked non-pointer. `PERRY_GC_VERIFY_EVACUATION=1` already fails loudly, so a shape-level assertion should localise it quickly.

**Ruled out** (all re-verified with genuine recompiles): `-Os` / #8457; #8418 in full (see my earlier correction — that attribution came from a bisect with an unverified good endpoint, my error); the `extern "C-unwind"` work; and the `js_put_value_set_dyn_ic` helper itself, whose miss path roots target/key/value in a `RuntimeHandleScope` and whose hit path cannot allocate. `property_key_receivers_survive_forced_evacuation` passes throughout, so receiver rooting is intact — the defect is specific to the **stored value** and the **proxy-forwarded set**.
```

## What you have

- `/testbed/repo` is a git clone of `PerryTS/perry` truncated just after the regression was
  reported.  `HEAD` is `caba324b710d878a60b6f20d5926536f7cad6756` and the full history behind it is present.
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
