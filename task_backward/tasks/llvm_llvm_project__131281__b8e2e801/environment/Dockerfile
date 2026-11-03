# llvm/llvm-project cut at 8727097ffd017ce55f39a3b7bc3788c6073e853d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2a48995a03ca5a615161565f24411dc11288bb3c \
        --stage baseline --out /opt/swe-time/receipt.json
