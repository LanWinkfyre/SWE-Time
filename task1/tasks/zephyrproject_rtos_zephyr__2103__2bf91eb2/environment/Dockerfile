# zephyrproject-rtos/zephyr cut at 1de77488ae543b119524cbc14344020c9f2eb43f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ae96c91109c81d600d58cc5870dd9e5cb336a3d3 \
        --stage baseline --out /opt/swe-time/receipt.json
