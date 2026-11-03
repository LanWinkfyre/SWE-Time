# vim/vim cut at 725310d89e1ba268bf410472b7de054c6c260161: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c2d09c9f2ce487a6971af9306e382d7b38805456 \
        --stage baseline --out /opt/swe-time/receipt.json
