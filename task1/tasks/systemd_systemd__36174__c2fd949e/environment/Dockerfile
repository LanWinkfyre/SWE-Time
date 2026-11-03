# systemd/systemd cut at 126f545a010ad4304fbcfb45c6893e7cb2f430fb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fc55da3d7c6fe7efa18f4341f581ef0c4f41803b \
        --stage baseline --out /opt/swe-time/receipt.json
