# systemd/systemd cut at f6301bdc81c7aca37fb21da877900ad0f9fbd49c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a86cbb0fa3ab5b0d87e62b0f59fe4cdd023b9587 \
        --stage baseline --out /opt/swe-time/receipt.json
