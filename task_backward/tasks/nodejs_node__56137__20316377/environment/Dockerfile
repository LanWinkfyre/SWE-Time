# nodejs/node cut at c4aa34aa4dc5accb100be07b4aceded83eeb3956: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 556f1aece2c21e39fafae13d2cf1832f5d4fcd59 \
        --stage baseline --out /opt/swe-time/receipt.json
