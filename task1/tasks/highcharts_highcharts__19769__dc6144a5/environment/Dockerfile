# highcharts/highcharts cut at 46b7f455a1174eb8b7a971be4c7f5a91fa1d85da: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ad99827d062e32ecf8f4c738f4c25f49b98c48ed \
        --stage baseline --out /opt/swe-time/receipt.json
