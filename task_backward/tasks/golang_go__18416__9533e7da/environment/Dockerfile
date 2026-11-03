# golang/go cut at 17190343e3db72a3f299e5a4359ae6bc3e5ed194: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f419b56354aee87c5173253e2d19cc51cc269f3c \
        --stage baseline --out /opt/swe-time/receipt.json
