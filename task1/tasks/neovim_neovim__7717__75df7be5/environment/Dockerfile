# neovim/neovim cut at 8813b29cec13f7410427fbb8913d3753dd6626a7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f976826690a975e03bb57f6cc84955c59ee6cff4 \
        --stage baseline --out /opt/swe-time/receipt.json
