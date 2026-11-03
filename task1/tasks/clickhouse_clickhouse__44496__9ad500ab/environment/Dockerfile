# ClickHouse/ClickHouse cut at f01fbc96817c0f4dca15c3418d444776b9221706: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe de33901c55c99052076877800d75c516488ae028 \
        --stage baseline --out /opt/swe-time/receipt.json
