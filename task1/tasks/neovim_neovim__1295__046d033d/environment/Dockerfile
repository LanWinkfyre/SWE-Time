# neovim/neovim cut at 0a2d9fa8c88b6e263b9baa9b639c23321272f9bf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 388e75e4b0f602ac5dd70e1ceeb1d1a18a37c51e \
        --stage baseline --out /opt/swe-time/receipt.json
