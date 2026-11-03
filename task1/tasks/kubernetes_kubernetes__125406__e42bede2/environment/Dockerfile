# kubernetes/kubernetes cut at d145bf09074fcd9b884daa582e0f19f60450a39d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b0263baae51895058b64b8e6f510a22a14ed8d3d \
        --stage baseline --out /opt/swe-time/receipt.json
