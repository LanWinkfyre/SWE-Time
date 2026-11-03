# neovim/neovim cut at 777cc6f98aa08ca4597658d0fb8b612a1c7c4c77: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6eab3b925016d6474bbf00671071414c7b0209c3 \
        --stage baseline --out /opt/swe-time/receipt.json
