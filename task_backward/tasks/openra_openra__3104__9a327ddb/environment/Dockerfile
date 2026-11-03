# OpenRA/OpenRA cut at 1db4cb186729179a4fc70facab547c25cb567e65: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0f519cf747226e8a95e13ed50d4b30d2c8db97f2 \
        --stage baseline --out /opt/swe-time/receipt.json
