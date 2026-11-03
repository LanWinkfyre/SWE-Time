# doxygen/doxygen cut at e321a870fda2c1c5bf759d6320b0063675f79fcd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bf95c6b396033e0ae29702ed3a2899a4cc4c8267 \
        --stage baseline --out /opt/swe-time/receipt.json
