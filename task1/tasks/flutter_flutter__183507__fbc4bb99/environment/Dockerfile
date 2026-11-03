# flutter/flutter cut at 640a089bb4ec8d10d469d19bec17ca1614dc093a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3f400d7c69e1dd25cd966206b83643a7c573a62f \
        --stage baseline --out /opt/swe-time/receipt.json
