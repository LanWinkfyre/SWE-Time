# bazelbuild/bazel cut at 7428006dd67cb6bd4e390253cc8ce89065792821: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2eb1bf53d5fef13b89ee440af4f83003d1d0b50a \
        --stage baseline --out /opt/swe-time/receipt.json
