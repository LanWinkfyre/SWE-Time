# zephyrproject-rtos/zephyr cut at f8b76f3b03dec540a6aeee7b176e0f01ef2b572f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c1ac125068a97383caf0ceb613418f7e23fd2085 \
        --stage baseline --out /opt/swe-time/receipt.json
