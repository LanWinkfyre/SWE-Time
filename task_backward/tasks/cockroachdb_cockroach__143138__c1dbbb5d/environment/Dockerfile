# cockroachdb/cockroach cut at 8c96475bf1e5af4a90b521ab66e34e67cc7faccc: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7c382176b8f595533e313e23b22650020a71e3c9 \
        --stage baseline --out /opt/swe-time/receipt.json
