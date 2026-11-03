# ggml-org/llama.cpp cut at c30e012253dd9e322c8e3424f808a5c74ecc46bf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe fbd441c37933550c1e3365dc84dd73232334c15d \
        --stage baseline --out /opt/swe-time/receipt.json
