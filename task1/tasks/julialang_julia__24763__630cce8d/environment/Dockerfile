# JuliaLang/julia cut at f8243b7d203a28c1ac4374f883fcb6d4d9667418: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6fa2047f1af1ad6d752302cb2992ad850a90718b \
        --stage baseline --out /opt/swe-time/receipt.json
