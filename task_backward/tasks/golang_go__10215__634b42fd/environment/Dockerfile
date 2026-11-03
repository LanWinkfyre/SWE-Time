# golang/go cut at 25bf792197ff737fc84c8b1dd46be8a6b066333a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a0fb8f8cce1d3b239f83c198204b616aab136510 \
        --stage baseline --out /opt/swe-time/receipt.json
