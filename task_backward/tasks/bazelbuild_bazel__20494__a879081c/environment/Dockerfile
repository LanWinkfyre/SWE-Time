# bazelbuild/bazel cut at 47e48a13563742473abdcaef46b7c4f222a86831: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 104a711ae1772be62b6034506d51c5fee486b589 \
        --stage baseline --out /opt/swe-time/receipt.json
