# highcharts/highcharts cut at c0dd6712d73fd73be9c67195a2ad65032ae684b5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f018501f76de18fa014070b52f618566934e825d \
        --stage baseline --out /opt/swe-time/receipt.json
