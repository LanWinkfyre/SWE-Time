# cockroachdb/cockroach cut at 43bfc3185cb362b14e0b8a331148f0b14542a4f2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d266989c4d30e6fbdc3fd6ac7458e7a651b87131 \
        --stage baseline --out /opt/swe-time/receipt.json
