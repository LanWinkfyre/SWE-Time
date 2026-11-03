# neovim/neovim cut at 807bc00dd68dccb55d5aa12e0a568d2551b08d04: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e91224bfaa043bb85cdfa6394f417e400522ff53 \
        --stage baseline --out /opt/swe-time/receipt.json
