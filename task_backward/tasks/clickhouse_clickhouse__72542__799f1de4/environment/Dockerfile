# ClickHouse/ClickHouse cut at ec914b108ed8464ca24a7e8e5a1fcd775f39a2c6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b4e5178dd069c11cd952c0b2a2af8c07d5440e16 \
        --stage baseline --out /opt/swe-time/receipt.json
