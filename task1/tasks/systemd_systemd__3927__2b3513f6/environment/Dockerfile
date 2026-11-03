# systemd/systemd cut at 3f193af8807be50913b87e1a5b88c494f8985667: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 87da8a864fd2173e176eb8b2f09b27711f1d3b5e \
        --stage baseline --out /opt/swe-time/receipt.json
