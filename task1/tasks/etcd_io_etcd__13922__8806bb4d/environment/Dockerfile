# etcd-io/etcd cut at 0c9a4e0f93ad9a7d83e8f5ec215baa856616c76b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe dd08e15d7c4750b1a94a8b4760a4de7fd14b0e78 \
        --stage baseline --out /opt/swe-time/receipt.json
