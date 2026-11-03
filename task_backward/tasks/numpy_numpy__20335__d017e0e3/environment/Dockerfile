# numpy/numpy cut at c280e21a74f2a6fd16d9c318696fcf167689baa3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0de29c58e3eede2bb65b51dbf72a93b767d04d49 \
        --stage baseline --out /opt/swe-time/receipt.json
