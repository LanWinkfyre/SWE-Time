# ClickHouse/ClickHouse cut at 79eb608ba11a1e8a832c46454143ad1e301dd097: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e42082b7eda6c48b34d1587f71ada8f5a5bfe93a \
        --stage baseline --out /opt/swe-time/receipt.json
