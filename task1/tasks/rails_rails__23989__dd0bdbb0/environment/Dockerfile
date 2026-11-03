# rails/rails cut at a408645223f81613b45366aa69d28584c37f17f8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8e3790c163b00af9c842602101dcb410361f5fd7 \
        --stage baseline --out /opt/swe-time/receipt.json
