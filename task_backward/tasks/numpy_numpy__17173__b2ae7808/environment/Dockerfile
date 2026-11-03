# numpy/numpy cut at 5bf6d68e7241498556ee1b28fc146c1c21fbb5e4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e4e0ab8e5ba9cdf17f9bd2c3c9e06e3d12030022 \
        --stage baseline --out /opt/swe-time/receipt.json
