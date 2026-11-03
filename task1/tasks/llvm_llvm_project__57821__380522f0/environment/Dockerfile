# llvm/llvm-project cut at 36f325413ec27819f8e4c1cd22d5f5e8a6a43000: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cd1d71c5f1a4595ea045a7a314fc33a6e093434e \
        --stage baseline --out /opt/swe-time/receipt.json
