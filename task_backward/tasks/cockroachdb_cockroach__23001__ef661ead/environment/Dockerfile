# cockroachdb/cockroach cut at efdf6a2673fa7e4fc158a9138b315e021d00fc39: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4933bb667a9aabeaaa90c0205db61a71f0ce33ea \
        --stage baseline --out /opt/swe-time/receipt.json
