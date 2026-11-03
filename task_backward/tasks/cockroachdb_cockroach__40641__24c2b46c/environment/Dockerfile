# cockroachdb/cockroach cut at a41355dabc985310e84ca32e890cd8318ff1f155: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 78599a151f4631ed23c87195a2aa15ee7f41ac69 \
        --stage baseline --out /opt/swe-time/receipt.json
