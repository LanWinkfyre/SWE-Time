# golang/go cut at 447965d4e008764a8635df6ca7d5d2e59c6d4229: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c53aecaaeaf8992bf8cafa7c8729228d7e4d2fee \
        --stage baseline --out /opt/swe-time/receipt.json
