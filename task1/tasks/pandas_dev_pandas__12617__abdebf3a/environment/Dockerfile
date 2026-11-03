# pandas-dev/pandas cut at ed3d1453f354a68999a4517f0e6641b11f2a9b9a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4f5099b4ee5f5c32f6b299de93902c9a074ac228 \
        --stage baseline --out /opt/swe-time/receipt.json
