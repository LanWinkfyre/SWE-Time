# zephyrproject-rtos/zephyr cut at d6f950c918715fe8b4de499b2ffc772b2d524f54: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 684ffd1e239fac4fab7928dbbda97cb1520f6865 \
        --stage baseline --out /opt/swe-time/receipt.json
