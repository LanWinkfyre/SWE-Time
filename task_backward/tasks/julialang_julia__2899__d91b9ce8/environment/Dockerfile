# JuliaLang/julia cut at 528e7f20e264e1f9e0cba812da1282d19ca11d86: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c624b0578c5e57e72afdfada9d8da6033c0553e1 \
        --stage baseline --out /opt/swe-time/receipt.json
