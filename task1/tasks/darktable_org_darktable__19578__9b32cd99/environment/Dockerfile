# darktable-org/darktable cut at 73ced28ae0d86504808d3bd2d9a0f8b5e084c448: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b603ad1d58fc8354ba416fa2dd0835b3438da5e9 \
        --stage baseline --out /opt/swe-time/receipt.json
