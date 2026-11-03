# scipy/scipy cut at f4263c24524f0b5ac5078056aa51721b8ca46392: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3d0b2b23ea8c4767a8eb4d8b3fc62fc6477e47be \
        --stage baseline --out /opt/swe-time/receipt.json
