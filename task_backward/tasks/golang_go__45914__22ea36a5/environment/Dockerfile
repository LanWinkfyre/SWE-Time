# golang/go cut at abb110bf3de82f85aefe0fb284cc9359488b5f09: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2c9f5a1da823773c436f8b2c119635797d6db2d3 \
        --stage baseline --out /opt/swe-time/receipt.json
