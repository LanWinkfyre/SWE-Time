#!/usr/bin/env python3
"""Trigger unit tests for the v4.1 Gold routing evaluator (诊断_0918.md section 10-B).

    python3 test_gold_routing.py

Every test is a workflow YAML evaluated under the FROZEN canonical context (action =
synchronize, non-draft, base_ref = the repository default branch).  These are the semantics the
Gold generator uses, so if any of them is wrong the whole benchmark is wrong -- run this before
trusting any Gold.
"""
from __future__ import annotations
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gold_routing import (_family_evaluates_active, _load, _pr_config,  # noqa: E402
                               _trigger_map, build_event_context)

PASS, FAIL = [], []


def check(name, cond, detail=""):
    (PASS if cond else FAIL).append(name)
    print(f"  {'PASS' if cond else 'FAIL'}  {name}" + (f"   [{detail}]" if detail and not cond else ""))


def active(yaml_text, changed, base="main"):
    wf = _load(yaml_text)
    fam, cfg = _pr_config(_trigger_map(wf))
    if fam is None:
        return False
    return _family_evaluates_active(cfg, changed, base)[0]


def main():
    print("== 10-B trigger unit tests (canonical action = synchronize) ==")

    # 1. types that exclude synchronize
    check("1. types:[closed] is INACTIVE under synchronize",
          not active("on:\n  pull_request:\n    types: [closed]\n", ["a.py"]))

    # 2. types that include synchronize
    check("2. types:[opened,synchronize] is ACTIVE under synchronize",
          active("on:\n  pull_request:\n    types: [opened, synchronize]\n", ["a.py"]))

    # 3. pull_request_target is an eligible family
    check("3. pull_request_target types:[synchronize] is ACTIVE",
          active("on:\n  pull_request_target:\n    types: [synchronize]\n", ["a.py"]))

    # 4. branches
    check("4a. branches:[main] with base_ref=main is ACTIVE",
          active("on:\n  pull_request:\n    branches: [main]\n", ["a.py"], "main"))
    check("4b. branches:[main] with base_ref=release is INACTIVE",
          not active("on:\n  pull_request:\n    branches: [main]\n", ["a.py"], "release"))

    # 4c. glob branch patterns
    check("4c. branches:[release-*] with base_ref=release-1.2 is ACTIVE",
          active("on:\n  pull_request:\n    branches: ['release-*']\n", ["a.py"], "release-1.2"))

    # 5. branches-ignore
    check("5a. branches-ignore:[main] with base_ref=main is INACTIVE",
          not active("on:\n  pull_request:\n    branches-ignore: [main]\n", ["a.py"], "main"))
    check("5b. branches-ignore:[legacy] with base_ref=main is ACTIVE",
          active("on:\n  pull_request:\n    branches-ignore: [legacy]\n", ["a.py"], "main"))

    # 6. paths
    check("6a. paths matching the change is ACTIVE",
          active("on:\n  pull_request:\n    paths: ['src/**']\n", ["src/x.py"]))
    check("6b. paths not matching the change is INACTIVE",
          not active("on:\n  pull_request:\n    paths: ['src/**']\n", ["docs/x.md"]))

    # 7. paths-ignore
    check("7a. paths-ignore covering the change is INACTIVE",
          not active("on:\n  pull_request:\n    paths-ignore: ['docs/**']\n", ["docs/x.md"]))
    check("7b. paths-ignore not covering the change is ACTIVE",
          active("on:\n  pull_request:\n    paths-ignore: ['docs/**']\n", ["src/x.py"]))

    # 8. combined types + branches + paths (all must pass)
    combo_ok = "on:\n  pull_request:\n    types: [synchronize]\n    branches: [main]\n    paths: ['src/**']\n"
    check("8a. combined: all three satisfied -> ACTIVE", active(combo_ok, ["src/x.py"], "main"))
    check("8b. combined: paths fails -> INACTIVE", not active(combo_ok, ["docs/x.md"], "main"))
    check("8c. combined: branches fails -> INACTIVE",
          not active(combo_ok, ["src/x.py"], "release"))
    combo_types = combo_ok.replace("types: [synchronize]", "types: [closed]")
    check("8d. combined: types fails -> INACTIVE",
          not active(combo_types, ["src/x.py"], "main"))

    # extra: excluded trigger families must not activate
    check("X1. push-only is INACTIVE",
          not active("on:\n  push:\n    branches: [main]\n", ["a.py"]))
    check("X2. workflow_dispatch-only is INACTIVE",
          not active("on:\n  workflow_dispatch:\n", ["a.py"]))
    check("X3. schedule-only is INACTIVE",
          not active("on:\n  schedule:\n    - cron: '0 0 * * *'\n", ["a.py"]))
    check("X4. bare `on: pull_request:` is ACTIVE (default activity includes synchronize)",
          active("on: pull_request\n", ["a.py"]))
    check("X5. `on:` as a list containing pull_request is ACTIVE",
          active("on: [push, pull_request]\n", ["a.py"]))
    check("X6. pull_request with no types but paths-ignore covering change is INACTIVE",
          not active("on:\n  pull_request:\n    paths-ignore: ['*.md']\n", ["README.md"]))

    # --- path patterns are anchored at the repository root (no implicit `**/` prefix)
    check("P1. paths 'backend/**' does NOT match a nested core/backend/ file",
          not active("on:\n  pull_request:\n    paths: ['backend/**']\n", ["core/backend/x.go"]))
    check("P2. paths 'backend/**' matches a root-level backend/ file",
          active("on:\n  pull_request:\n    paths: ['backend/**']\n", ["backend/x.go"]))
    check("P3. paths-ignore 'backend/**' does NOT ignore core/backend/ (workflow ACTIVE)",
          active("on:\n  pull_request:\n    paths-ignore: ['backend/**']\n", ["core/backend/x.go"]))
    check("P4. paths-ignore 'gallery/**' does NOT ignore core/gallery/ (workflow ACTIVE)",
          active("on:\n  pull_request:\n    paths-ignore: ['gallery/**']\n", ["core/gallery/a.go"]))
    check("P5. paths '**/docs/**' still matches a nested docs/ directory",
          active("on:\n  pull_request:\n    paths: ['**/docs/**']\n", ["pkg/docs/a.md"]))
    check("P6. paths '*.md' does NOT match a nested docs/a.md (`*` stops at `/`)",
          not active("on:\n  pull_request:\n    paths: ['*.md']\n", ["docs/a.md"]))
    check("P7. paths '**.md' matches a nested docs/a.md",
          active("on:\n  pull_request:\n    paths: ['**.md']\n", ["docs/a.md"]))
    check("P8. paths 'src/*' does NOT match src/a/b.py",
          not active("on:\n  pull_request:\n    paths: ['src/*']\n", ["src/a/b.py"]))
    check("P9. branches 'release-*' still matches 'release-1.2'",
          active("on:\n  pull_request:\n    branches: ['release-*']\n", ["a.py"], "release-1.2"))

    # --- `!` negation: ordered, last matching pattern wins
    neg = "on:\n  pull_request:\n    paths: ['src/**', '!src/doc/**']\n"
    check("N1. paths with !exclusion: excluded-only change is INACTIVE",
          not active(neg, ["src/doc/x.md"]))
    check("N2. paths with !exclusion: non-excluded change is ACTIVE",
          active(neg, ["src/a.py"]))
    check("N3. paths re-include after ! wins (last match decides)",
          active("on:\n  pull_request:\n    paths: ['src/**', '!src/doc/**', 'src/doc/keep.md']\n",
                 ["src/doc/keep.md"]))
    check("N4. paths-ignore with !: re-included file keeps workflow ACTIVE",
          active("on:\n  pull_request:\n    paths-ignore: ['docs/**', '!docs/api/**']\n",
                 ["docs/api/x.md"]))
    check("N5. paths-ignore with !: fully ignored change is INACTIVE",
          not active("on:\n  pull_request:\n    paths-ignore: ['docs/**', '!docs/api/**']\n",
                     ["docs/guide.md"]))
    check("N6. branches with !: excluded branch is INACTIVE",
          not active("on:\n  pull_request:\n    branches: ['release-*', '!release-old']\n",
                     ["a.py"], "release-old"))

    # --- event-context construction and consumption
    ctx = build_event_context({"default_branch": "main", "base_sha": "a" * 40})
    check("E1. build_event_context sets action=synchronize", ctx["action"] == "synchronize")
    check("E2. build_event_context resolves base_ref from the case metadata",
          ctx["base_ref"] == "main")
    check("E3. base_ref provenance names the base SHA", "a" * 12 in ctx["base_ref_source"])
    check("E4. eligible families are exactly pull_request + pull_request_target",
          ctx["eligible_trigger_families"] == ["pull_request", "pull_request_target"])
    check("E5. context is serialisable and round-trips",
          json.loads(json.dumps(ctx)) == ctx)
    ctx2 = build_event_context({"default_branch": "master", "base_sha": "b" * 40})
    check("E6. a different default branch produces a different base_ref",
          ctx2["base_ref"] == "master")
    check("E7. everything except base_ref is identical across cases",
          {k: v for k, v in ctx.items() if k not in ("base_ref", "base_ref_source")}
          == {k: v for k, v in ctx2.items() if k not in ("base_ref", "base_ref_source")})

    print(f"\nGOLD_ROUTING_V4_1_UNIT_TESTS: {len(PASS)} passed, {len(FAIL)} failed")
    if FAIL:
        print("FAILED:", FAIL)
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
