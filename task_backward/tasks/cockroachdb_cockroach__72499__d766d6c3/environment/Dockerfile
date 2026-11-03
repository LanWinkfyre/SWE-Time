# cockroachdb/cockroach cut at 46b7efa32c57b15f4ae6e0d75845f63360b62161: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a0849b11188efd1c58dc339d15f75b03e0762459 \
        --stage baseline --out /opt/swe-time/receipt.json
