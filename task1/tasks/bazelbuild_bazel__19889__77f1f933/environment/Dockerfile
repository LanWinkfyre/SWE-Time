# bazelbuild/bazel cut at 073fba498cd436fdf99067ed8bdcb023c78c7200: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a4a73c526edcdbf675d34a25b1c397744d700e05 \
        --stage baseline --out /opt/swe-time/receipt.json
