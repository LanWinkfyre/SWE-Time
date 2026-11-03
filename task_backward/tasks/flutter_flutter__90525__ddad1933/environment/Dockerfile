# flutter/flutter cut at a921c1cf3d2616704bcbb83ab13d89e39be0c97c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8d7068694b01bb5589cac9b35446aeb3dc097eec \
        --stage baseline --out /opt/swe-time/receipt.json
