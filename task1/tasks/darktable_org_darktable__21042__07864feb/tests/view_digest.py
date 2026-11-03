#!/usr/bin/env python3
"""Recompute Stage-2's `view_digest` from a materialized package.

`view.digest_of` hashes the sorted list of *visible* tracked paths, where visible means
"not matched by artifacts.is_hidden".  Porting that matcher here would be a second copy
of a rule that must not drift, so instead the set is derived from the filesystem: the
package self-check already proved that exactly the hidden paths are absent and no ordinary
path was over-removed, so "tracked and present on disk" is the same set by construction.
Verified byte-identical on prometheus_prometheus__5321__27bb4757 (3583 paths).
"""
import hashlib
import os
import subprocess
import sys

repo = sys.argv[1]
listing = subprocess.run(["git", "-C", repo, "ls-files", "-s", "-z"],
                         capture_output=True).stdout.decode("utf-8", "surrogateescape")
visible = []
for record in listing.split("\0"):
    fields = record.split("\t", 1)
    if len(fields) == 2 and not fields[0].startswith("160000"):
        # lexists, not exists: some repos track symlinks pointing outside the checkout.
        if os.path.lexists(os.path.join(repo, fields[1])):
            visible.append(fields[1])
payload = "\n".join(sorted(visible)).encode("utf-8", "surrogateescape")
print(hashlib.sha256(payload).hexdigest())
