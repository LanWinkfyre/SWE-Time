# flutter/flutter cut at 565e48777ab207c1cce241f704f14b20b4e258f3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7e02cc34f9ea4647eaaeef8475eb88003bbc6f2b \
        --stage baseline --out /opt/swe-time/receipt.json
