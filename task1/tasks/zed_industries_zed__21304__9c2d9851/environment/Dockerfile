# zed-industries/zed cut at 3458687300e6d226531019738ad0669993b5c17d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe eb2c0b33dff361a268b0276f8ec8bb38811d2c5e \
        --stage baseline --out /opt/swe-time/receipt.json
