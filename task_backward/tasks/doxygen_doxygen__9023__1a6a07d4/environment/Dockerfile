# doxygen/doxygen cut at 1f1ac2838cfcc8e4bd95501df4d7376d35a0848e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ed118033fe2fbc229646209fa0dd3cb4e39c257b \
        --stage baseline --out /opt/swe-time/receipt.json
