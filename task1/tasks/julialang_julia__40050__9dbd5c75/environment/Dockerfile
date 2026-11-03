# JuliaLang/julia cut at 8fc52931fca94f4247f2b0e8f69447f8417d70ab: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 70b6afa4328d2c4a0aef4c432c85a30eca83aadb \
        --stage baseline --out /opt/swe-time/receipt.json
