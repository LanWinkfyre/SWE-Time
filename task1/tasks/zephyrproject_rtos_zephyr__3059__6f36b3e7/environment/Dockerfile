# zephyrproject-rtos/zephyr cut at 916837c22ca8050417a6dd4503b991a8a74aafdd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 466c2fc7ec8564f0b0c2ad04c49fb5ccfacbef13 \
        --stage baseline --out /opt/swe-time/receipt.json
