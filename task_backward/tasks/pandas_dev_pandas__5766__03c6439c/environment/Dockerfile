# pandas-dev/pandas cut at 2485e0934e90c2f3bd16967c3d36b0cd3b8413bf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 62c41537061fa77be3ee59f07eaf5dcf5a54913c \
        --stage baseline --out /opt/swe-time/receipt.json
