# pandas-dev/pandas cut at 702be31ec71b2fe4ec40b72b9bc06804fd1a7373: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2dad23f766790510d09e66f1e02b57a395d479b1 \
        --stage baseline --out /opt/swe-time/receipt.json
