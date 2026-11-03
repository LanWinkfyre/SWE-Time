# highcharts/highcharts cut at 51620ae161b3bd25b00088b85ec5e74062f831d8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0e52f3f7fa83b057a68c44ceb1e40237d486813d \
        --stage baseline --out /opt/swe-time/receipt.json
