# pandas-dev/pandas cut at 0e857ffebec8f96a8723e7cd09bee2e356d90e26: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 79e3ee6fce8830cc8c1ca8166bf49af8f369095b \
        --stage baseline --out /opt/swe-time/receipt.json
