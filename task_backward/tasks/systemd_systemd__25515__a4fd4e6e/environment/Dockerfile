# systemd/systemd cut at fe5779cf3f939d8e1ed21ab621dddde0b6699874: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 03288a3f286db73d913716e9506df452fd1b77cb \
        --stage baseline --out /opt/swe-time/receipt.json
