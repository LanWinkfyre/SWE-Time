# dotnet/runtime cut at ca6fb31c65e7c26d1d3096133a1d862bd8af086d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 044caf66bc78f7f1a6f18b532ed343fcc99fa680 \
        --stage baseline --out /opt/swe-time/receipt.json
