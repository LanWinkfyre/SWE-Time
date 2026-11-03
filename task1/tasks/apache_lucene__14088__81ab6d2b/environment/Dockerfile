# apache/lucene cut at c0fc70016e1d79da96aa57d2799d5c9ded8cbb8d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 525b963be076fe8c58dd1162f083b6a9911e4efd \
        --stage baseline --out /opt/swe-time/receipt.json
