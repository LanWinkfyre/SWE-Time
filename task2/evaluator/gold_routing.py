#!/usr/bin/env python3
"""Task 2 Protocol v4.1 — deterministic Gold routing evaluator.

    from gold_routing_v4_1 import CANONICAL_E, effective_workflows, resolve_default_branch

Given

    historical fixing scope Δ*  +  repository @ S_t  +  canonical evaluation context E

produce the **Effective Gold Workflow Set**: the repository-relative paths of the workflows that
would be DIRECTLY activated by the prospective fix.

This replaces the v2 rule, which asked only whether the literal key `on.pull_request` existed and
then consulted `paths` / `paths-ignore`.  Two whole classes of Gold entry were wrong because of it,
in opposite directions:

  * INCLUDED but unreachable — `pull_request: {types: [closed]}` fires when a PR is MERGED, not
    when it is updated; `branches: [release-*]` cannot match a PR targeting `main`.  A model
    applying real Actions semantics excluded them and was charged a false negative.
  * EXCLUDED but reachable — `pull_request_target` fires on the same PR event (with a different
    token and base checkout).  A model that included it was charged a false positive.

Both came from recognising exactly one literal key.  This module models the event properly.
"""
from __future__ import annotations
import re

# --------------------------------------------------------------------------- frozen context
# E is benchmark-wide and identical for every case; the ONLY repo-resolved field is base_ref.
CANONICAL_E = {
    "activity": "pull_request_update",
    "action": "synchronize",
    "draft": False,
    "activation_scope": "direct",
    "eligible_trigger_families": ("pull_request", "pull_request_target"),
}
# GitHub's default activity types for the pull_request family when `types:` is not declared.
DEFAULT_PR_ACTIVITY = ("opened", "synchronize", "reopened")


def glob_match(pattern: str, value: str) -> bool:
    """GitHub filter patterns are globs, NOT regular expressions, matched against the whole
    value (branch name or repo-relative path).  Per GitHub's filter cheat sheet, `*` and `?`
    do not match `/`; `**` matches any characters including `/`."""
    out, i, n = [], 0, len(str(pattern))
    p = str(pattern)
    while i < n:
        c = p[i]
        if c == "*":
            if i + 1 < n and p[i + 1] == "*":
                out.append(".*"); i += 2
            else:
                out.append("[^/]*"); i += 1
        elif c == "?":
            out.append("[^/]"); i += 1
        elif c == "[":
            j = i + 1
            neg = j < n and p[j] in "!^"
            if neg:
                j += 1
            if j < n and p[j] == "]":
                j += 1
            k = p.find("]", j)
            if k == -1:
                out.append(r"\["); i += 1
            else:
                cls = p[j:k]
                out.append("[^" + re.escape(cls) + "]" if neg else "[" + re.escape(cls) + "]")
                i = k + 1
        else:
            out.append(re.escape(c)); i += 1
    try:
        return re.fullmatch("".join(out), value) is not None
    except re.error:
        return False


def _trigger_map(wf):
    """Normalise `on:` to a dict.  GitHub accepts three shapes and all three occur in the wild:
    a mapping, a list (`on: [push, pull_request]`), and a bare scalar (`on: push`)."""
    on = wf.get("on")
    if isinstance(on, list):
        return {k: None for k in on}
    if isinstance(on, dict):
        return on
    if isinstance(on, str):
        return {on: None}
    return {}


def _pr_config(trig, event_context=None):
    """Return (family, config) for the highest-priority eligible trigger family present."""
    fams = (event_context or CANONICAL_E)["eligible_trigger_families"]
    for fam in fams:
        if fam in trig:
            return fam, trig[fam]
    return None, None


def build_event_context(row: dict) -> dict:
    """Resolve the ONE event context a case uses, and serialise it.

    Every field except `base_ref` comes from the frozen protocol constant.  `base_ref` is the
    repository's default branch AT S_t, taken from the case's harvested metadata -- captured
    per-case at the base SHA by the Stage-2 mirror refresh, never from current HEAD and never from
    the fixing PR.

    The returned dict is the single object that BOTH the prompt and the Gold generator consume:
    it is written into the case artifact, rendered into the instruction, and handed to
    `effective_workflows`.  Keeping one serialised object rather than two equivalent-looking
    parameter lists is what makes "the model and the grader saw the same context" a checkable
    property instead of a promise.
    """
    base_ref = (row.get("default_branch") or "main").strip()
    return {
        "activity": CANONICAL_E["activity"],
        "action": CANONICAL_E["action"],
        "base_ref": base_ref,
        "draft": CANONICAL_E["draft"],
        "activation_scope": CANONICAL_E["activation_scope"],
        "eligible_trigger_families": list(CANONICAL_E["eligible_trigger_families"]),
        "base_ref_source": f"default_branch @ {row.get('base_sha', '?')[:12]} (harvested at S_t)",
    }


def _filter_hit(patterns, value, match) -> bool:
    """GitHub filter-list semantics: patterns are evaluated in order and the LAST pattern that
    matches decides; a leading `!` makes a pattern exclude.  `['src/**', '!src/doc/**']` hits
    `src/a.py` but not `src/doc/x.md`."""
    hit = False
    for pat in patterns:
        pat = str(pat)
        if pat.startswith("!"):
            if match(pat[1:], value):
                hit = False
        elif match(pat, value):
            hit = True
    return hit


def _family_evaluates_active(config, changed_paths, default_branch, action=None):
    """> (active, reason).  `config` is the value under one pull_request-family key."""
    action = action or CANONICAL_E["action"]
    if config is None or config == {} or isinstance(config, list):
        return True, None                      # declared with no constraints -> fires
    if not isinstance(config, dict):
        return False, "malformed trigger config"

    types = config.get("types")
    if isinstance(types, list) and types:
        if action not in types:
            return False, f"types={types} excludes '{action}'"
    # no `types:` -> GitHub's default activity set, which includes synchronize

    branches = config.get("branches")
    if isinstance(branches, list) and branches:
        if not _filter_hit(branches, default_branch, glob_match):
            return False, f"branches={branches} excludes '{default_branch}'"
    branches_ignore = config.get("branches-ignore")
    if isinstance(branches_ignore, list) and branches_ignore:
        if _filter_hit(branches_ignore, default_branch, glob_match):
            return False, f"branches-ignore={branches_ignore} covers '{default_branch}'"

    paths = config.get("paths")
    if paths is not None:
        if not any(_filter_hit(paths, cp, _path_hit) for cp in changed_paths):
            return False, "paths do not match the change"
    paths_ignore = config.get("paths-ignore")
    if paths_ignore is not None:
        if changed_paths and all(_filter_hit(paths_ignore, cp, _path_hit)
                                 for cp in changed_paths):
            return False, "paths-ignore covers the change"
    return True, None


def _path_hit(pattern, path) -> bool:
    """GitHub matches `paths` / `paths-ignore` patterns against the full path from the
    repository root.  There is no implicit `**/` prefix: `backend/**` matches
    `backend/x.go` but not `core/backend/x.go`.  The frozen v4.1 evaluator added that prefix
    to every pattern not starting with `*`, which widened both filters."""
    return glob_match(str(pattern), path)


def effective_workflows(fs, changed_paths, event_context):
    """> (set of activated workflow paths, {path: reason} for the eligible ones that are NOT).

    `fs` is any object with `.listdir(".github/workflows")` and `.read(path)`; the packaged
    `WorktreeFS` and the adapter's MirrorFS both qualify.  `event_context` is the serialised
    object produced by `build_event_context` -- the same one rendered into the prompt.
    """
    active, inactive = set(), {}
    for name in fs.listdir(".github/workflows"):
        if not name.endswith((".yml", ".yaml")):
            continue
        rel = f".github/workflows/{name}"
        text = fs.read(rel)
        wf = _load(text)
        if not isinstance(wf, dict):
            inactive[rel] = "unparseable"
            continue
        trig = _trigger_map(wf)
        fam, cfg = _pr_config(trig, event_context)
        if fam is None:
            inactive[rel] = "no eligible pull_request trigger family"
            continue
        ok, reason = _family_evaluates_active(cfg, changed_paths, event_context["base_ref"],
                                              event_context["action"])
        if ok:
            active.add(rel)
        else:
            inactive[rel] = f"{fam}: {reason}"
    return active, inactive


def _load(text):
    """Parse with the YAML 1.1 bool resolver DROPPED, or `on:` becomes the key True."""
    if text is None:
        return None
    try:
        import yaml
    except ImportError:                                        # pragma: no cover
        return None
    class Loader(yaml.SafeLoader):
        pass
    for key in list(Loader.yaml_implicit_resolvers):
        Loader.yaml_implicit_resolvers[key] = [
            (tag, rx) for tag, rx in Loader.yaml_implicit_resolvers[key]
            if tag != "tag:yaml.org,2002:bool"]
    try:
        return yaml.load(text, Loader=Loader)
    except Exception:                                          # noqa: BLE001
        return None


def resolve_default_branch(row: dict, fs=None) -> str:
    """The default branch AT S_t.  Thin wrapper kept for callers that only need the value."""
    return build_event_context(row)["base_ref"]
