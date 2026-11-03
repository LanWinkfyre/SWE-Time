# ggml-org/llama.cpp cut at 8afe2280009ecbfc9de2c93b8f41283dc810609a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 92d0b751a77a089e650983e9f1564ef4d31b32b9 \
        --stage baseline --out /opt/swe-time/receipt.json
