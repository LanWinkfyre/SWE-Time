# zephyrproject-rtos/zephyr cut at 433893e54b9ca7e70d6f158690839b56913d5dce: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f902f2ab0d24fab4a98536e422258522191132b7 \
        --stage baseline --out /opt/swe-time/receipt.json
