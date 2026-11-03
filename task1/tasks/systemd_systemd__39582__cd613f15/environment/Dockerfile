# systemd/systemd cut at fea7f5d68b5a6272ce8989e872a57b42121b5205: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b1aa33ff916d67d54103474e81ca612e3d4b9e59 \
        --stage baseline --out /opt/swe-time/receipt.json
