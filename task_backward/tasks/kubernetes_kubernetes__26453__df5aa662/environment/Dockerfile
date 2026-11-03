# kubernetes/kubernetes cut at 1cca499e9222e8a44cce7b637ac2ff7031c6f290: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cddf564f3cde57ba672f0643bd8fdc3eef0f682e \
        --stage baseline --out /opt/swe-time/receipt.json
