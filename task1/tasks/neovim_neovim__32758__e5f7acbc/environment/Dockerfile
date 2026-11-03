# neovim/neovim cut at 7371abf7554ebbcdb66bde3c892954596c497ff4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e46f07b1d2942c7b5c08fca9a4cac735ee2c0c71 \
        --stage baseline --out /opt/swe-time/receipt.json
