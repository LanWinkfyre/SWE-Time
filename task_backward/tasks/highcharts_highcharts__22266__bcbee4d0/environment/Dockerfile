# highcharts/highcharts cut at 6cbbb6317a756821daea6af2c3f56db8e35c7167: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3ccee8d59de2b745ebcb23e4523c53cbbbd78a53 \
        --stage baseline --out /opt/swe-time/receipt.json
