# cockroachdb/cockroach cut at c5474dd14a5b626fbc920201bacdf19f37694c95: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7437e29908c1544a587c4e6315d21e474f21caf2 \
        --stage baseline --out /opt/swe-time/receipt.json
