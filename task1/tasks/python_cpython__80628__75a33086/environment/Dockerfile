# python/cpython cut at bc284f0c7a9a7a9a4bf12c680823023a6770ce06: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1fc5bf2ff27b898e8d9460d0fbc791e83009ed71 \
        --stage baseline --out /opt/swe-time/receipt.json
