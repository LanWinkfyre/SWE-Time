# ClickHouse/ClickHouse cut at 217363d9a766bacbf0acae88118dff1055dbbaa9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7d03fd98bd28490fd773aabaddec37f23f2fdf8f \
        --stage baseline --out /opt/swe-time/receipt.json
