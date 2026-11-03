# python/cpython cut at af2afd7c224389856e118d3f544c9621a016599f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8bd88e2827b2a887c2ea8e5ed0c0575704bfacdf \
        --stage baseline --out /opt/swe-time/receipt.json
