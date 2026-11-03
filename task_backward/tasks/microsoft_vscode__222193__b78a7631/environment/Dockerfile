# microsoft/vscode cut at 37898a5689f24f6fb14e4942eb2a18ead0eb4358: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 08c88cee367ada58c34f852b6cded88dfe321499 \
        --stage baseline --out /opt/swe-time/receipt.json
