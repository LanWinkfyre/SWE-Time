# neovim/neovim cut at bb185d63ab86e305e35603297a88c0ec8fba27ae: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe aa853f362addded400d52d8fdfe5247c300c0e89 \
        --stage baseline --out /opt/swe-time/receipt.json
