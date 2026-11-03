# microsoft/vscode cut at 89c4f61de26b4682d4de44c6c5f7801cf0f261cf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a1e73c96a47d9139eb3965a00a1f682a74ec7bcd \
        --stage baseline --out /opt/swe-time/receipt.json
