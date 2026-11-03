# zephyrproject-rtos/zephyr cut at 3ebd9b4a09dcf26ec689c3a2ae9eb241201cd1ef: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7aa98f7196fb4e465f3306fd7d77ed9d82ed3b6d \
        --stage baseline --out /opt/swe-time/receipt.json
