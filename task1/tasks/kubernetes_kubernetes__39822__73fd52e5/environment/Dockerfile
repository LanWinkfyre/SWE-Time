# kubernetes/kubernetes cut at 1854d48238b289fa7ac41adfc8dba09cd0f3ce1a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ee49906c45171b1da354910bce4f4ed2095dd0d4 \
        --stage baseline --out /opt/swe-time/receipt.json
