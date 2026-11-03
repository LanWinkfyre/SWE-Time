# systemd/systemd cut at 7655550a49056dffaf7e834386ff4cc59bfb4f1a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5495b11360d649dc8810d59b096231ba596e9436 \
        --stage baseline --out /opt/swe-time/receipt.json
