# JuliaLang/julia cut at a526a4a4b3e9afc648320291c6242d99b364667f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fec8304a8c6e2157759b76d20339b426201a5f61 \
        --stage baseline --out /opt/swe-time/receipt.json
