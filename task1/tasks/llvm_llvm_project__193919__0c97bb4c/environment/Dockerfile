# llvm/llvm-project cut at 340ba1191cfc49588119a93724f5c26810ddc1a6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c55a73c44e4af903ded70aec5c8d6af1cb312440 \
        --stage baseline --out /opt/swe-time/receipt.json
