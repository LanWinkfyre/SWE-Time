# bazelbuild/bazel cut at 4d916c505d932ddd473bccafb84fb97ec97cc69d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ecb88370ed8f4b8c233328f06e47251f71d14b1a \
        --stage baseline --out /opt/swe-time/receipt.json
