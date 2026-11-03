# vim/vim cut at a91871262670f9d3a4e5d1c5c6dbc02f85625f7d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe de05ae71589f46c5d27642c33fe5eb21b22aaf5d \
        --stage baseline --out /opt/swe-time/receipt.json
