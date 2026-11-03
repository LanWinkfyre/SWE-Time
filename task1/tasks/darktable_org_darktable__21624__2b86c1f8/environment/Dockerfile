# darktable-org/darktable cut at 73b039cfe145463525c1f286470f3d000563712b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe efd4805a56a2c058f9d14e25d21d37f6ae866cc8 \
        --stage baseline --out /opt/swe-time/receipt.json
