# golang/go cut at 071b8d51c1a70fa6b12f0bed2e93370e193333fd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5d36bc18d56fa5d7ad10b675dd82892ed3100332 \
        --stage baseline --out /opt/swe-time/receipt.json
