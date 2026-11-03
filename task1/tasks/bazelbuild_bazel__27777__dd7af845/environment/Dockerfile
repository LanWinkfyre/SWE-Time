# bazelbuild/bazel cut at 25f91f948a84de1b9158dea8904a98b671e76ed5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a63c6d8d4b96d17e38aa29da20d5cba952843098 \
        --stage baseline --out /opt/swe-time/receipt.json
