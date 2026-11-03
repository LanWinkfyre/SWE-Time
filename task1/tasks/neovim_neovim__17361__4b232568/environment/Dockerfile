# neovim/neovim cut at a73360a09a54c186f2df6e167a8be1f1a1d8c62a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c2ec3664e02543e08625694471e9f6dd254539ba \
        --stage baseline --out /opt/swe-time/receipt.json
