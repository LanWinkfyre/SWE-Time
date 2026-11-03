# darktable-org/darktable cut at c728e0314ff8cdda962c546bd7af8cf2af234d78: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 93903b0931950b354dce41f910a41f14b48aafe5 \
        --stage baseline --out /opt/swe-time/receipt.json
