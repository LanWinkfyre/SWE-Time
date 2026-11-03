# highcharts/highcharts cut at 28bfd585f3a4b3acc3a153bea50a19cc2dc21d47: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7a8422425c43985e31a2807e33d6d23bde2a5e33 \
        --stage baseline --out /opt/swe-time/receipt.json
