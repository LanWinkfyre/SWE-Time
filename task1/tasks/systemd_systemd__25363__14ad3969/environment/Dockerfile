# systemd/systemd cut at e48237358fd21e26722506c5cf89c99f2c40a90f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0d217f634958ec15fa062ad182ff851284119579 \
        --stage baseline --out /opt/swe-time/receipt.json
