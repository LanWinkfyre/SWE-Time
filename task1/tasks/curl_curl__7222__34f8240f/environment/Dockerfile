# curl/curl cut at 92c588f04b2da0e6e96d5b9640e83a8efc4bf281: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cd5ca9bb384e04713744e35cc009b40c40eaf67c \
        --stage baseline --out /opt/swe-time/receipt.json
