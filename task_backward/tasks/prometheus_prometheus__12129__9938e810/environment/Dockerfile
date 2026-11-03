# prometheus/prometheus cut at 6c008ec56af958debf4123d7cd58a6681d17303d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bec68558ba991d28e706d3eaa0b2c4576ab9c9f6 \
        --stage baseline --out /opt/swe-time/receipt.json
