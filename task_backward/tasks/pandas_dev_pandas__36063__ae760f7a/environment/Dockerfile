# pandas-dev/pandas cut at 73c1d3269830d787c8990de8f02bf4279d2720ab: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1fc244f89108347804ea33c7e912f933c2aa63da \
        --stage baseline --out /opt/swe-time/receipt.json
