# bazelbuild/bazel cut at 50bf666652aacd274d534ad4ec4eadf8e8452e05: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9f68000c9c2a93d24150066f70140b52de15a1cf \
        --stage baseline --out /opt/swe-time/receipt.json
