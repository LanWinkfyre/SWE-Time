# curl/curl cut at cc9bf974cd8dc53fbb24d6f7a6dc558c71bff5bd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1ba0d4bdb39e8fff541484afaee8a1f308a12018 \
        --stage baseline --out /opt/swe-time/receipt.json
