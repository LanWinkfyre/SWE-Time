# prometheus/prometheus cut at d390497280d61918aa8792f87a2f458e5e231ec2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 901b82d94c531b4dd9b0e3977a12b8d185180eff \
        --stage baseline --out /opt/swe-time/receipt.json
