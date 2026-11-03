# microsoft/vscode cut at e5054d1d42fb0d3ea6f5b4ba95545c26375847eb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f528f1a415557a530a36a44a8b2675b6bd2575a0 \
        --stage baseline --out /opt/swe-time/receipt.json
