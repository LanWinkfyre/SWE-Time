# rails/rails cut at 737b718ea0c88d3f6c139343f957f386e06fffc9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8925e37fdcc37f4ff2ab2d55168719bbe9386ebf \
        --stage baseline --out /opt/swe-time/receipt.json
