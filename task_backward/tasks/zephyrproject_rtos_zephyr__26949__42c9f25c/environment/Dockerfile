# zephyrproject-rtos/zephyr cut at 5092541e2b59f4a319520d677a59b706cd3bd665: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4df734683e2aec5f3287bc5eedeb5bb2a1f9a6e5 \
        --stage baseline --out /opt/swe-time/receipt.json
