# JuliaLang/julia cut at ec807bc01ccd53c4dac07dcce4bfb25a20d38f20: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6919ddf1d71157028456e75708607cb3c01edd3d \
        --stage baseline --out /opt/swe-time/receipt.json
