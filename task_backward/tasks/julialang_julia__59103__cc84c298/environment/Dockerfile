# JuliaLang/julia cut at c5ba4e28f2c9c49be01ed7409efedef8627fe96d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d5fdf04cb2c903c6fffa3db5da199ba1fce83065 \
        --stage baseline --out /opt/swe-time/receipt.json
