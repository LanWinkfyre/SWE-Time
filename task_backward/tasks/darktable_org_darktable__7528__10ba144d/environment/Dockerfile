# darktable-org/darktable cut at f755cfc283773cc084495006bdf5a31c17ae4ff1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fed21e2b67b2d7b19def692fc637c93b46a98feb \
        --stage baseline --out /opt/swe-time/receipt.json
