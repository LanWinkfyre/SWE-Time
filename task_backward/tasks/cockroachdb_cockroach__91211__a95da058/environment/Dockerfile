# cockroachdb/cockroach cut at 3013bc561480c5bcabdaf0d4ae80cea717f3267e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3fd47f1fa8e4541828af6e0d5ebb8020420c5a2a \
        --stage baseline --out /opt/swe-time/receipt.json
