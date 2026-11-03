# nodejs/node cut at a5b87305255f4757545b1d9f60a5e6f94cb742c8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7ff2170f3660f60656a13476969e6cc9bb96b7d9 \
        --stage baseline --out /opt/swe-time/receipt.json
