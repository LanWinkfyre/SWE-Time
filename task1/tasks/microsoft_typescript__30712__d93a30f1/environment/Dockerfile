# microsoft/TypeScript cut at 0830292633790a6a50a494589ac0efd0f500b59c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bf0dd79e4acb03ec30f742f13c02c3a6bb868674 \
        --stage baseline --out /opt/swe-time/receipt.json
