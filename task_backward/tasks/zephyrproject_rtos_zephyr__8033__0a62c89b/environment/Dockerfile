# zephyrproject-rtos/zephyr cut at 55494c3f0a9c9ea6ddd2ab20940dd2afafd16c71: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe aa26d9926af7e1e31da0b39b4a89a8c11d0ff42e \
        --stage baseline --out /opt/swe-time/receipt.json
