# flutter/flutter cut at 4f02152cec641e91d37f23f50c2e52cc4108f57b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1f8bc5f225493c247d4348e6a9ad4e41d3641033 \
        --stage baseline --out /opt/swe-time/receipt.json
