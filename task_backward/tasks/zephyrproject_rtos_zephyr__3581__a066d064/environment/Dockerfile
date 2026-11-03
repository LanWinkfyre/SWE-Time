# zephyrproject-rtos/zephyr cut at 6c2eff60668b0538808af79a2a4bbb52d012ac79: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6c9e563c92001674db247aa409bd424fa613984b \
        --stage baseline --out /opt/swe-time/receipt.json
