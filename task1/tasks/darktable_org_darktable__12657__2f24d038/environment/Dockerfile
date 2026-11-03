# darktable-org/darktable cut at afb0ac5c003544bfa239ecaf6f93b0cc7d82e171: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 22078abbb8dfe7cfb305ad6b788d17c1660b345a \
        --stage baseline --out /opt/swe-time/receipt.json
