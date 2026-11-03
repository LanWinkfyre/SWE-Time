# doxygen/doxygen cut at b09c7316acaa5e8dc6d34bd69c1aba381c6d818c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 853197f9823c2d928b2760634c3d602fc705e8a3 \
        --stage baseline --out /opt/swe-time/receipt.json
