# flutter/flutter cut at 29d59e3cb7dcd74a8e6ecb57c5c2b11fa106cba0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 66e3f9d8aac26b4124afac65d693b415057f6a10 \
        --stage baseline --out /opt/swe-time/receipt.json
