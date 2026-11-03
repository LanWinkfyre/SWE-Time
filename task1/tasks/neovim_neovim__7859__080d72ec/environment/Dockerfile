# neovim/neovim cut at c06995b34d604a37f80ee1174fcb3530dbd59206: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 60d6a8b13d2eb5cdc5ab2740a9becc3b24e1eb71 \
        --stage baseline --out /opt/swe-time/receipt.json
