# flutter/flutter cut at 2a063fc6c06063d1b4686703f094e489baca6cee: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7bef51acc979ee467c02a7503a8990a6edbb0ae3 \
        --stage baseline --out /opt/swe-time/receipt.json
