# openssl/openssl cut at 21f4bd986b7739f24f67270d533412065c7af0fc: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8e08f9c5a013d9a9fb9e2db3c90a70eda50f78b5 \
        --stage baseline --out /opt/swe-time/receipt.json
