# darktable-org/darktable cut at de2cf0f4162ba2d5bb0144967ae1f27307fd5ae5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b2995917b067bf703c2ac46e6e954fe5f1e224a8 \
        --stage baseline --out /opt/swe-time/receipt.json
