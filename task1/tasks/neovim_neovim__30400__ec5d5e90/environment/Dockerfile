# neovim/neovim cut at a0d8c2b86e788ce4273f0b8df258cd9e8e432d38: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0ade8fed143dd8cf3ca0571eb4ed66ff27bc0325 \
        --stage baseline --out /opt/swe-time/receipt.json
