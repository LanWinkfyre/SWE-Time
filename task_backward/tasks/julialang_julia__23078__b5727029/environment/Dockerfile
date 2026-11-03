# JuliaLang/julia cut at fb76529050cdf142ce6614b28d690fff560e8d3a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 18da73e62f6ef7ae3e8acc0b10d109abacee814c \
        --stage baseline --out /opt/swe-time/receipt.json
