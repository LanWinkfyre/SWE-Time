# zephyrproject-rtos/zephyr cut at 581261334c36135ce384ce660ccef498b2c0d39f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1c171ec283481eb6b02d4f7fd7dff84f93eee636 \
        --stage baseline --out /opt/swe-time/receipt.json
