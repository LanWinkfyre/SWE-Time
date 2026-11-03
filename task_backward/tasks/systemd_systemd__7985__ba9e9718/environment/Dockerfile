# systemd/systemd cut at 420d2058674b8f0edb6c135c125df0781b87d964: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 21112e594c02ba283d9953075cf7b0a18d1e9228 \
        --stage baseline --out /opt/swe-time/receipt.json
