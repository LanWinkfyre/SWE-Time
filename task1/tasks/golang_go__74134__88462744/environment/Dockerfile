# golang/go cut at 934d5f2cf703c6aad9f0ce6a73a3922d1af83049: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9149876112facc113d77d2c65e1590184c57d0c2 \
        --stage baseline --out /opt/swe-time/receipt.json
