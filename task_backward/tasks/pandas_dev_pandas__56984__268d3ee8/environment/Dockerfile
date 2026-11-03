# pandas-dev/pandas cut at 5849cc7c3bfded6a1ebc3ad46f621268ed8d97cf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 21b3906a39eca5ba8220d5e34ca1f204a68a5adb \
        --stage baseline --out /opt/swe-time/receipt.json
