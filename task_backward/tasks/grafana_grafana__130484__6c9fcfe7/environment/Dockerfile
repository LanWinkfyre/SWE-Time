# grafana/grafana cut at e6cf001c19890a110b4f2677776988793d02f14a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4054c0644cde47008aafc6d5a5085a9197c3d020 \
        --stage baseline --out /opt/swe-time/receipt.json
