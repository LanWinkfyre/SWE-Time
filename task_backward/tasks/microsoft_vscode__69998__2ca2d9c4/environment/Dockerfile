# microsoft/vscode cut at 7333aa8aee07946b2f4906a17ec6ce7e95b5155b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d88074401953a85018de40f075a095d3496a5d4c \
        --stage baseline --out /opt/swe-time/receipt.json
