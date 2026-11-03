# zephyrproject-rtos/zephyr cut at a8b742362e1986fea7300ab73b774cdaba0d7066: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9c8a6099a76f0d4b36fccd1195b5b53eda330a20 \
        --stage baseline --out /opt/swe-time/receipt.json
