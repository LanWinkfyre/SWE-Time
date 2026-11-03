# flutter/flutter cut at ceaac22da1a1558eb623d95ba81afd7aa349d9e0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1a578b583e2b0bf5a8125deae417128751000c9c \
        --stage baseline --out /opt/swe-time/receipt.json
