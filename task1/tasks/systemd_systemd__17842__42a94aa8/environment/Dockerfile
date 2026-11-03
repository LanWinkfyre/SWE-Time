# systemd/systemd cut at 6dd16814a56d2ce96ab3c4c611a61e47f2f7b663: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e267d76f732c6b7f3e7b02259ac5173e1781e267 \
        --stage baseline --out /opt/swe-time/receipt.json
