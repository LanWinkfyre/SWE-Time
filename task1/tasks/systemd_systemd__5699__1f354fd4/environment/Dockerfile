# systemd/systemd cut at 77d3bb1200b1a49e3d5cec82749a139dbd06075c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 91dacd4451309e1f4b06fb2628447ddc8425d972 \
        --stage baseline --out /opt/swe-time/receipt.json
