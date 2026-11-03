# JuliaLang/julia cut at 7eb1edb73e09445e89edc96d09e827fa1f2464fd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7bd100978463c10734d14eb74d157c37602e584d \
        --stage baseline --out /opt/swe-time/receipt.json
