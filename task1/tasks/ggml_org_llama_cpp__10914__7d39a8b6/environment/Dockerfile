# ggml-org/llama.cpp cut at d408bb9268a988c5a60a5746d3a6430386e7604d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0a11f8b7b5c39fdf6e91ef9674bc68ff08681af7 \
        --stage baseline --out /opt/swe-time/receipt.json
