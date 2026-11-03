# PerryTS/perry cut at caba324b710d878a60b6f20d5926536f7cad6756: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8d1cca158641b272c3b7ddea74515e6c4ff18c0c \
        --stage baseline --out /opt/swe-time/receipt.json
