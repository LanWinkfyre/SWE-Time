# highcharts/highcharts cut at 8b71b62df6bf5292c4014e7fea3bde392886598b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0d4ef8642c16f2e4a0c9276ad415f13c40aeff1a \
        --stage baseline --out /opt/swe-time/receipt.json
