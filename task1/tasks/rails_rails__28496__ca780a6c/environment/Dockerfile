# rails/rails cut at 5c0d00072d1309dbc77bb5d97e42956bac3e8684: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 34e85c461ceb1f8cc4a0e0e3299b20246bee4c79 \
        --stage baseline --out /opt/swe-time/receipt.json
