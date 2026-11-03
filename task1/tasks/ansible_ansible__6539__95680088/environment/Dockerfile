# ansible/ansible cut at 9da26da335924f1fe4dd8fae94780dbfccbe4269: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7c5ad1fa230ff1f64aaf56442926c16ce16ccc5b \
        --stage baseline --out /opt/swe-time/receipt.json
