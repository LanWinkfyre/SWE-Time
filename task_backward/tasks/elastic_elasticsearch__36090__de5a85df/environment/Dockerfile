# elastic/elasticsearch cut at 78e07d467c87e4728734b0da1ebc50f43109175e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 14eeb2aa30d4c4456acc44a0b5923867ecf95d70 \
        --stage baseline --out /opt/swe-time/receipt.json
