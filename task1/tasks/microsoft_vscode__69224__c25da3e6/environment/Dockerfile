# microsoft/vscode cut at eee10d2c7f79e05526e555c9a39d57d835d5a40d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 85618de788fafde00cb00c40cc7af49d972a47fc \
        --stage baseline --out /opt/swe-time/receipt.json
