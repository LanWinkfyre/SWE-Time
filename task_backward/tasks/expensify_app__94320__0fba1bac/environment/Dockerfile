# Expensify/App cut at 1d88d349ddaa8ff17d0c1e5e16e9adb9c0a2e3a1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 21d10c5dbbe1d7740b44dd5bdcfec80eda6afe6b \
        --stage baseline --out /opt/swe-time/receipt.json
