# pandas-dev/pandas cut at 0d07c2361b13a24afc7cd2bf91e642474f313195: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe dafa5dd84acc1ba1b2641fd0bb6d3ca3594a5e9e \
        --stage baseline --out /opt/swe-time/receipt.json
