# pandas-dev/pandas cut at fd1c3f868d2d8f8763cf126054ebbb5ae367017a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 68b1da7f53f043b21e3f722e8872e19941a10250 \
        --stage baseline --out /opt/swe-time/receipt.json
