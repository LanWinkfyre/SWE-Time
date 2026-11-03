# flutter/flutter cut at 6067d8f2195d303fca946ae5400c05cc82f2e2e7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 03e6cfa7b193fce922e3e313e6ad24643a425cfc \
        --stage baseline --out /opt/swe-time/receipt.json
