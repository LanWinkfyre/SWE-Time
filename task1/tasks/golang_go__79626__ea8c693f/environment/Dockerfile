# golang/go cut at 5078670ed22e5b69c3b45d015333e5a1d58c8788: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 24ec7d2120d3d16b79cb2a7009a3e8025e4a2ce4 \
        --stage baseline --out /opt/swe-time/receipt.json
