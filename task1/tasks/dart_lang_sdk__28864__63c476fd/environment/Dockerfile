# dart-lang/sdk cut at cdda898b3cf85e66d41a6570e1d1a1c277903521: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 46cacfeae93310b09b52d8fca2b8f9348f230a5e \
        --stage baseline --out /opt/swe-time/receipt.json
