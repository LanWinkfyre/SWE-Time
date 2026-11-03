# flutter/flutter cut at 12de94d152ad14c0cdf2aa615f5050fdd6be3329: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe aa3436db7ae35ec48c4f4aaf78236ab6e350a958 \
        --stage baseline --out /opt/swe-time/receipt.json
