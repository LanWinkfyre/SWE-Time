# zephyrproject-rtos/zephyr cut at d820dddaab31c7c1752f4f2ecb61dc1c59063b34: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d15d346bbf7c2c6cb493088b876c56be63ff9878 \
        --stage baseline --out /opt/swe-time/receipt.json
