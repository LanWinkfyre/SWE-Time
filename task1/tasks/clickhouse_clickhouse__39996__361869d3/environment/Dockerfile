# ClickHouse/ClickHouse cut at 2a62910fb59fd8bcc21e183d4aab208ba6661003: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4c3153b2bac617683631cc88b6411b5f5618ec7b \
        --stage baseline --out /opt/swe-time/receipt.json
