# bazelbuild/bazel cut at 5c1c0d1ed8643c90fba239d1bc642e4ebd044c2c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4eada72fcfbd37c62673d353d3b0c70c4b7345f7 \
        --stage baseline --out /opt/swe-time/receipt.json
