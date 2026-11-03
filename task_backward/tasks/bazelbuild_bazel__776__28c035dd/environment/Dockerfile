# bazelbuild/bazel cut at 8c40daa91818926460e9c917371bec74fd80c339: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 37265a87c7aa9743a2b20069be85d03529b18534 \
        --stage baseline --out /opt/swe-time/receipt.json
