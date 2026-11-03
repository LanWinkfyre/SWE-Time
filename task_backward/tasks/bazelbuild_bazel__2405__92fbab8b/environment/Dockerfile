# bazelbuild/bazel cut at 4e267c86afc8ce0a6c33c0cb851f519ccd20b650: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 214542fe4c23b8aa962e1aab1241c65310730990 \
        --stage baseline --out /opt/swe-time/receipt.json
