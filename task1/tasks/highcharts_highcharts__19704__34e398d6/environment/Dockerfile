# highcharts/highcharts cut at 0a045faee69f61563ddbbefb86d435ec1975c667: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe da8b03d08727a4aa4437ed794adad80c5158f5c1 \
        --stage baseline --out /opt/swe-time/receipt.json
