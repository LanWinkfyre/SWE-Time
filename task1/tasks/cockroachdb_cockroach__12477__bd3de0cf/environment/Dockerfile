# cockroachdb/cockroach cut at 17b99047a726d5c3c4d8bf595812a27abdaf16ff: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6a08e4e92c338f3b4d70457c31ff0aa67e1b2d3e \
        --stage baseline --out /opt/swe-time/receipt.json
