# cockroachdb/cockroach cut at cea63881b16ab19260a590e2dbf4f405881bd70e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f1a5aa8a633636138fededdf46a8dcc20f899a48 \
        --stage baseline --out /opt/swe-time/receipt.json
