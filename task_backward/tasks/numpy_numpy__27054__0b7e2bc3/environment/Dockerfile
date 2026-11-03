# numpy/numpy cut at 2459d80adf7d8e7c0c6debf72f5207a6ca37f264: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6af7bf2932a34b21ad42840db566d00e76ec6b7a \
        --stage baseline --out /opt/swe-time/receipt.json
