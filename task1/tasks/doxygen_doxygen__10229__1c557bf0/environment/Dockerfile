# doxygen/doxygen cut at 682b594f5b4334512dc2f3026be5c4e0d90fb6a1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 473dcba15aa9b20ce07fcc9e1e6783557d9231d2 \
        --stage baseline --out /opt/swe-time/receipt.json
