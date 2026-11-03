# microsoft/vscode cut at 112bd0900270e49b27b81e8c06a1f44227901a82: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 17c67963f3245c7e6c753ac4a223a2e5f07b61f0 \
        --stage baseline --out /opt/swe-time/receipt.json
