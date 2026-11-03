# JuliaLang/julia cut at efd7f94b7b126ecfc3e6157a7c89091af8d6705d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ad854b6596f7d535b4ec80fe5d65e0e2303eaae7 \
        --stage baseline --out /opt/swe-time/receipt.json
