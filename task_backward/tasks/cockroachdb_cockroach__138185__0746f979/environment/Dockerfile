# cockroachdb/cockroach cut at 5207cd59f4cfd8444cb3d7739f53063bed4ae1a6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e132eba1ff28b44b62c29fec26f61dfc740bee1a \
        --stage baseline --out /opt/swe-time/receipt.json
