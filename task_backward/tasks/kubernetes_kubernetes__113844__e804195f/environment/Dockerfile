# kubernetes/kubernetes cut at cf12a74b18b66efc577ec819c78a0c68f6d49225: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d7bff1c80912b20bc969111ac52825b67909bbe8 \
        --stage baseline --out /opt/swe-time/receipt.json
