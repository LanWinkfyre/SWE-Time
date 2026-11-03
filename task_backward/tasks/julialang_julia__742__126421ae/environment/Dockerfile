# JuliaLang/julia cut at b3251fe0e53f6c01396e16aae51c49cbdebee26e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 05981460780fb15d73723e03b6d112e8b03c6dc3 \
        --stage baseline --out /opt/swe-time/receipt.json
