# cue-lang/cue cut at 8bcd577f27b2f86bcb7143717520924c6c96ffe1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe dbc027a80da44ae6bd53d311ed009502cd8d3856 \
        --stage baseline --out /opt/swe-time/receipt.json
