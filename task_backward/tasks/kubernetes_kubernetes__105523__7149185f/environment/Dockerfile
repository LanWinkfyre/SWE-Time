# kubernetes/kubernetes cut at a861de6d162f6197971dffbf09ae101545a9c2e7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe dbd8d3bcd620037b5262eed1778f0784b49e55bc \
        --stage baseline --out /opt/swe-time/receipt.json
