# darktable-org/darktable cut at 92e04f41a6595b3fd2df3bcc1a6bb70ea12f807b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 19ee56a2bf87b89a43f2377c5c60d214687623f4 \
        --stage baseline --out /opt/swe-time/receipt.json
