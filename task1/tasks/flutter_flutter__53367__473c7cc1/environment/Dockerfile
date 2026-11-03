# flutter/flutter cut at c9f999278cf3d7e1fb3d36feea36664325834095: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0d111bc91a0861b1a689c807f6c732cac1292c51 \
        --stage baseline --out /opt/swe-time/receipt.json
