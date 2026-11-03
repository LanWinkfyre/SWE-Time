# zephyrproject-rtos/zephyr cut at 74a32bdff3ca6f8ba1acaae05b223488fbbc81af: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a0fa5f80a7d0e20faf0bfab690d6b466919a6cd6 \
        --stage baseline --out /opt/swe-time/receipt.json
