# pandas-dev/pandas cut at e033c0616158d3ba974456b4f84810492936b1fe: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cc8d33e00bcf7d1e0bf08f58ffae3f16d37ff118 \
        --stage baseline --out /opt/swe-time/receipt.json
