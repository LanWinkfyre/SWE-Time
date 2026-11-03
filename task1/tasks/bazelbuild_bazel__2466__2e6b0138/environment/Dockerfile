# bazelbuild/bazel cut at bef4fbed3d22a976b895a3f75ad41699747c286e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 62dbdfec3d7f6effc182f2e15f84acf0b6fa2f72 \
        --stage baseline --out /opt/swe-time/receipt.json
