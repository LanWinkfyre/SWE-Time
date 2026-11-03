# pandas-dev/pandas cut at 89ddd8a70ede962dfcff01cf21f375b88fc8098b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe aa25da2d79b4503fe0f82b08b3cfb25130623138 \
        --stage baseline --out /opt/swe-time/receipt.json
