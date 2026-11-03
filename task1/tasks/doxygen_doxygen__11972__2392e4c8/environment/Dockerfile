# doxygen/doxygen cut at e02b26a8101beafedebc953503fd208931f4e38d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6d17f1f58e1af7d708713eed4de57964a31392cc \
        --stage baseline --out /opt/swe-time/receipt.json
