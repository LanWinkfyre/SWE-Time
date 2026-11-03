# ansible/ansible cut at 17b3171917d85dd622bc96366bbdfecf8498718d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0d068f1e3afe21a81295584bfb8ddd621bc54e8d \
        --stage baseline --out /opt/swe-time/receipt.json
