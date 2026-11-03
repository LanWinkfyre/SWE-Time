# OpenRA/OpenRA cut at eb09870a103d8f8a2f6fe07aa30085888e93b269: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c07af73eaefd535b3558c8119e365c36ac4e0b63 \
        --stage baseline --out /opt/swe-time/receipt.json
