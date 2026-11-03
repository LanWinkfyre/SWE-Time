# zephyrproject-rtos/zephyr cut at d66e8077cef9c22f5dc09628ae1436a529a35472: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 734eda39f5868207bb6a9d0eba346d24e153eba3 \
        --stage baseline --out /opt/swe-time/receipt.json
