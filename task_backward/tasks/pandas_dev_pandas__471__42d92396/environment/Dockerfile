# pandas-dev/pandas cut at cc463925b7b5991ec3e900c1c68f09e66dcc31a8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8b0f22f634d73204195718afa00bd8816b2d9269 \
        --stage baseline --out /opt/swe-time/receipt.json
