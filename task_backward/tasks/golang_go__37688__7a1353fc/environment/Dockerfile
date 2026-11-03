# golang/go cut at 585e31df63f6879c03b285711de6f9dcba1f2cb0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cc6a8bd0d7f782c31e1a35793b4e1253c6716ad5 \
        --stage baseline --out /opt/swe-time/receipt.json
