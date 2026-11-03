# highcharts/highcharts cut at 53d9bed3abd49e160290fad5c95ffa446fe72244: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c12832e25851afca07fb5485d5427775f8c24a48 \
        --stage baseline --out /opt/swe-time/receipt.json
