# ansible/ansible cut at 45355cd5660da17350811d92a5144077910ea434: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 19af43ed5d00a9b827c8056610c78d3e52fa840b \
        --stage baseline --out /opt/swe-time/receipt.json
