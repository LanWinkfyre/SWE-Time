# ggml-org/llama.cpp cut at 79fe79919436fa26029a0ac1ea25eb34c2c2fb0d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0adcc3bb571011bff8b91335d0728a82845c421b \
        --stage baseline --out /opt/swe-time/receipt.json
