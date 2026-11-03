# pandas-dev/pandas cut at 1ee5ecf3ddbf1ce92e1a78e90a4ef07fc3cf0840: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d623ffd90f57abda2beb34d807da58ca95b3743d \
        --stage baseline --out /opt/swe-time/receipt.json
