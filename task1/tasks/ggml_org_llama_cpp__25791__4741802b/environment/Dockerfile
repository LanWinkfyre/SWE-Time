# ggml-org/llama.cpp cut at e8f19cc0ad70a243c8012bf17b4be601abfc8ea2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b85833e934123f373a8dc087316e385b28c98cc0 \
        --stage baseline --out /opt/swe-time/receipt.json
