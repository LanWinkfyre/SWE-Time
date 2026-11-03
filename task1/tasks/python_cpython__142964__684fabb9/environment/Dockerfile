# python/cpython cut at 1391ee664c8f019996e0cbf658e12fa38abd211d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 220f0b107776391201a399c54dd01692c36fcdf4 \
        --stage baseline --out /opt/swe-time/receipt.json
