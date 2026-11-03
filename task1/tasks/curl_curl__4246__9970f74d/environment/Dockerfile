# curl/curl cut at 862393243d16870347e56195e93dc47274e32601: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6a90c9e0c49dc8179f6ff60bdfe1bd59aa55ef7b \
        --stage baseline --out /opt/swe-time/receipt.json
