# zephyrproject-rtos/zephyr cut at ad7beb530a05388748e2c307ac4176dd139eb7ef: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9aeb7e7669076ac41df2a9943c90b1fee8450e38 \
        --stage baseline --out /opt/swe-time/receipt.json
