# numpy/numpy cut at fe6f42c427239d36579723085cc5207cedd8dcd1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c5ccca92c5f136833ad85614feb2aa4f5bd8b7c3 \
        --stage baseline --out /opt/swe-time/receipt.json
