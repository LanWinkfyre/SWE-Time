# apache/lucene cut at 346d7624db510c3bc2cb9012f6a01f29d98ac5de: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 182208e84b034b9634ce5e25393488b5f417f8df \
        --stage baseline --out /opt/swe-time/receipt.json
