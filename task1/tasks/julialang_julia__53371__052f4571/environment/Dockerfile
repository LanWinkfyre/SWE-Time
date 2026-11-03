# JuliaLang/julia cut at 93876c92ed725272d8853d73dc0c3256095f1617: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 199851801fa183c1bfac9b3ba2282655e2629b7f \
        --stage baseline --out /opt/swe-time/receipt.json
