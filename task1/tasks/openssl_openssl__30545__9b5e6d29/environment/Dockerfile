# openssl/openssl cut at d3951537462175218d1e8a553e93fffb7cc1facb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5efde2afedb23b12c7f42c8f6a1daa37a617220d \
        --stage baseline --out /opt/swe-time/receipt.json
