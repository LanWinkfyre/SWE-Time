# JuliaLang/julia cut at 495a004bda33e284b0acc612f5ced9ba1eb9a777: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f00d729c16c80e6e090505144e454ec655601bb8 \
        --stage baseline --out /opt/swe-time/receipt.json
