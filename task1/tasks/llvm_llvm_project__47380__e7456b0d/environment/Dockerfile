# llvm/llvm-project cut at 799033d8c569616fbf7c829f2e9b01d5adf4cd6f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 63ad0876567d7a782daedfe9f564942a37f063f5 \
        --stage baseline --out /opt/swe-time/receipt.json
