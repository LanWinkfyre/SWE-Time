# highcharts/highcharts cut at 7d12b6296615ffdc7cc976b54db5c23038b37d01: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4a6108d5413b76fa97c21b63bb261cb22ea63340 \
        --stage baseline --out /opt/swe-time/receipt.json
