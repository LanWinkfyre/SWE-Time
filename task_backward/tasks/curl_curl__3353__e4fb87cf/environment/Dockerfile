# curl/curl cut at d997aa0e963c5be5de100dccdc5208d39bd3d62b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1e9abfedfa7a858d89233088c503ebec4762b9fa \
        --stage baseline --out /opt/swe-time/receipt.json
