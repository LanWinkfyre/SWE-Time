# doxygen/doxygen cut at 10b2b8fc694b60a17ccd2642f3a40c851e33b9da: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 96f87f11a303fb2f5b563e7f277df55336e2bb39 \
        --stage baseline --out /opt/swe-time/receipt.json
