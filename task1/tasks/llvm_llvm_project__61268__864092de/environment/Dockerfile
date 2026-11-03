# llvm/llvm-project cut at e65cd4ce832b52d7b625a1e01cbecb264f9d2716: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7fb0b1b8d7e75c442b4ae2f1564e1e703aca98b4 \
        --stage baseline --out /opt/swe-time/receipt.json
