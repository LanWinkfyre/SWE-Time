# ggml-org/llama.cpp cut at bd60d82d0cc8b6852ec535495a5042dbdf05de24: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 47cc7a7bf9793f81a6dfe7c2096c499403f64dd6 \
        --stage baseline --out /opt/swe-time/receipt.json
