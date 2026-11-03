# OpenRA/OpenRA cut at 33e779f4c0d75366e41400dc98885afd3dbf6db7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9d32667d1543170fd14d57f865039f86fd706b17 \
        --stage baseline --out /opt/swe-time/receipt.json
