# flutter/flutter cut at 45e4a0e5250c8ed21aa2d13fc2ce668aba11f186: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 528a281a5c89c9bb91e6c6d1f90ebc1376a3809b \
        --stage baseline --out /opt/swe-time/receipt.json
