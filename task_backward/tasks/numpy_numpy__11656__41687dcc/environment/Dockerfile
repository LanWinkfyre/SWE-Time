# numpy/numpy cut at e14db2f4fcbcf030701a0410a1d647edfa5f0261: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 066298b46f5d63ba6c144c4750444cde9a983b87 \
        --stage baseline --out /opt/swe-time/receipt.json
