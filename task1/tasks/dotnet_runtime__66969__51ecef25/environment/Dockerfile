# dotnet/runtime cut at 7a01e0f14f8df4992b046096093224ce53ec7a59: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cde8b0b6a0aa81f0af75b9adf55ebea4591ddee4 \
        --stage baseline --out /opt/swe-time/receipt.json
