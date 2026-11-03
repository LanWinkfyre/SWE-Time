# zephyrproject-rtos/zephyr cut at f2e0f787bf83da84cd8f31d86ca214ef290c8d70: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 82024ad5cf31bf3b2b9848754e89b4014811b4d6 \
        --stage baseline --out /opt/swe-time/receipt.json
