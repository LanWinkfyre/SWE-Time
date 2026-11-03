# bazelbuild/bazel cut at 97eaf9136abad30827cf1a060cc32e786745923d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4be230a125c07a918d6d4f4b03be6cafbaaa30c5 \
        --stage baseline --out /opt/swe-time/receipt.json
