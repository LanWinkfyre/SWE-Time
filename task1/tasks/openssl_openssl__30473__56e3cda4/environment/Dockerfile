# openssl/openssl cut at 40f076965f154e307a0821088b6adcc447ceae01: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f56a9fa69db773cfdf9af68e5b8a65067b015077 \
        --stage baseline --out /opt/swe-time/receipt.json
