# numpy/numpy cut at 18c13458d544d9b935b63e7b495a346ec14f5468: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4f549ea3b2eb25d0622530280b18474ff47dac9f \
        --stage baseline --out /opt/swe-time/receipt.json
