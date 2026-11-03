# flutter/flutter cut at b74fa8afc7e2365f96098e6ff0fb150beb22682a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f0a37e70e550277f5879f41e8b4e3dc493d7c218 \
        --stage baseline --out /opt/swe-time/receipt.json
