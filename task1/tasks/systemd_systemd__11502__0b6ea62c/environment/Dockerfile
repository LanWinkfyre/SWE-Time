# systemd/systemd cut at 8464d9e0dc506538fd0f2d1d667966750cb9cf30: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4b8183c153cc177fec1ecb3631a1c51dc710bcc6 \
        --stage baseline --out /opt/swe-time/receipt.json
