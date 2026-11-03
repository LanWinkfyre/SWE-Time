# neovim/neovim cut at 9b0b3a0883ab6c9d9f57fcf65d5bc951f40dff3c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 130611fca3900276d4525e17ded47504d73b38a1 \
        --stage baseline --out /opt/swe-time/receipt.json
