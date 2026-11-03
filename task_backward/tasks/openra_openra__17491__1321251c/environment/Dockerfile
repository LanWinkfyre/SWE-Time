# OpenRA/OpenRA cut at bb85146544b85b4be8a3514cfed06f68d4b42f46: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5830d4de6cc6d43164cb20ad8e630e0f289a6088 \
        --stage baseline --out /opt/swe-time/receipt.json
