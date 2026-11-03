# OpenRA/OpenRA cut at 75c105cb853bb76bba53b3c44839927271022d39: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cebf908bb2e6589ac62f039dbd70aaedd7f806e0 \
        --stage baseline --out /opt/swe-time/receipt.json
