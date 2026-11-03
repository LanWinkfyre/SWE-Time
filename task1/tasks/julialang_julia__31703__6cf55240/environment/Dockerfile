# JuliaLang/julia cut at 20834c3176bf1cfd29096f72f49bb63de0d7b02d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1aa8c6821bab79bfe1a2e99008ebd9b22323a2d0 \
        --stage baseline --out /opt/swe-time/receipt.json
