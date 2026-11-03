# llvm/llvm-project cut at 8b222ecf2769ee133691f208f6166ce118c4a164: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 63f5235978568421adecba44af88cca0a13019c2 \
        --stage baseline --out /opt/swe-time/receipt.json
