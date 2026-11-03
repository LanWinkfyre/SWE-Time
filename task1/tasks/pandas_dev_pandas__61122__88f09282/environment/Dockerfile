# pandas-dev/pandas cut at 8943c97c597677ae989d47e612705f088aab4cd0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5d9cf431f7b774a6724b1dd4c5e6f6fe95647aff \
        --stage baseline --out /opt/swe-time/receipt.json
