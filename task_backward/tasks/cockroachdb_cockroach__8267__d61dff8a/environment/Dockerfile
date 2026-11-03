# cockroachdb/cockroach cut at b23939d8e080250174ca5a2c25f5dd3e71df1dce: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 47802111b0098c18e69b2b578804ed484d9c0305 \
        --stage baseline --out /opt/swe-time/receipt.json
