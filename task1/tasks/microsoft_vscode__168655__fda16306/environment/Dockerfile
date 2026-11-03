# microsoft/vscode cut at 09b5220d78ed381fa02ca56b1fd4dbd5777a7e7a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 67c997d6a65a3c857e9e2e589d3b4adf5ee1ff34 \
        --stage baseline --out /opt/swe-time/receipt.json
