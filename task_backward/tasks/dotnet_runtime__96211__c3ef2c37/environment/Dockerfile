# dotnet/runtime cut at 8bd23f0792c6339478222ebc6635266e8f4098b4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1e8f0b347f7ab125e07ac6004c3c02929ad569c5 \
        --stage baseline --out /opt/swe-time/receipt.json
