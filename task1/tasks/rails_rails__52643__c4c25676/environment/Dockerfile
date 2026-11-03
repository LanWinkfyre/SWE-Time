# rails/rails cut at 16882b886e245f363cd61f5ea553fe2bc525d070: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 607d61e884237c223c24c6f47efa0b561dd8b637 \
        --stage baseline --out /opt/swe-time/receipt.json
