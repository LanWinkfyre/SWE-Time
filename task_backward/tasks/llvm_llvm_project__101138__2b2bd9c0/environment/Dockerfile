# llvm/llvm-project cut at fcd6bd5587cc376cd8f43b60d1c7d61fdfe0f535: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe abc2fe31fc622c4eab3766d739576110eb6f16c3 \
        --stage baseline --out /opt/swe-time/receipt.json
