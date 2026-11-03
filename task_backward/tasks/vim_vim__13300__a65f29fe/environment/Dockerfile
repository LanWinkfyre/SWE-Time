# vim/vim cut at 2a281ccca017fb5e8ffd20a86aa390431224a2fd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1087b8c29ab521106c5b6cc85d5b38244f0d9c1d \
        --stage baseline --out /opt/swe-time/receipt.json
