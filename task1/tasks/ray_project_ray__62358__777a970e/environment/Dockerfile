# ray-project/ray cut at 5de7691678bff3b56c73f6b8c5f5a2904c182b82: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ccf2ed3eb9887378546bdbfc63c53e3964a28e68 \
        --stage baseline --out /opt/swe-time/receipt.json
