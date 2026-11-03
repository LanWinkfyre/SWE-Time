# zed-industries/zed cut at 54a95e717d4ed1589c9b0e38648f65424defc74b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d72a03827d4bfa85c404cc846b6fa7d6b0537220 \
        --stage baseline --out /opt/swe-time/receipt.json
