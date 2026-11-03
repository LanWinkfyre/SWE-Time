# zed-industries/zed cut at a56a260778748c1309c5a30d37a917f10e56c39d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2abb5aeaf22840e505bd1a119a0fef458d8a15b2 \
        --stage baseline --out /opt/swe-time/receipt.json
