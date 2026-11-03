# cockroachdb/cockroach cut at 24c961f5c222bfc1b34be3fce44624c1d5aa0ad1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bfa4eb4546f07af040fdd5ae66dfc2ab642acac8 \
        --stage baseline --out /opt/swe-time/receipt.json
