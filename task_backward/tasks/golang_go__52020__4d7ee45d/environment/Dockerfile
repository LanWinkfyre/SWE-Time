# golang/go cut at a4a0f9b1481e9be4361eb9c4998eca08e2eedb0a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe dac0220841a44815584c83d26e9f9a45f5560f6d \
        --stage baseline --out /opt/swe-time/receipt.json
