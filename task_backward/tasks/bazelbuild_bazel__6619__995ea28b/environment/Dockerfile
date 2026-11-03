# bazelbuild/bazel cut at 91e0bae6143e39f60e9d62e8b61854cbc8d7a4f4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4e87e2f994a3350b5c7540ccf18340e41fa454ad \
        --stage baseline --out /opt/swe-time/receipt.json
