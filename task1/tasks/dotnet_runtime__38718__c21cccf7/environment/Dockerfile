# dotnet/runtime cut at 106cd9ebaed5f974fa8f17e153ec3e22b6576f43: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8126962457be677cb8b9313d5d9f26849da77df2 \
        --stage baseline --out /opt/swe-time/receipt.json
