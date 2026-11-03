# JuliaLang/julia cut at 0fb601aa3075f488ae5e468ae0a5267717188164: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 32bf6862306fac0392071912c795045bf98765d9 \
        --stage baseline --out /opt/swe-time/receipt.json
