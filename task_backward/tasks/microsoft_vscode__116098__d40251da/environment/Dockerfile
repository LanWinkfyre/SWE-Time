# microsoft/vscode cut at d0205792b0e01ae323cd9c7ef4c10b517e820da4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9dd25c4d196e2920027afa5645003e6ccf245248 \
        --stage baseline --out /opt/swe-time/receipt.json
