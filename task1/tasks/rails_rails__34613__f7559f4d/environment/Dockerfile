# rails/rails cut at 609c58bfa6df58b88e3eadebb1f1d49354541d24: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e5172265bf36c0834a67ef82c0ad514cfe7671df \
        --stage baseline --out /opt/swe-time/receipt.json
