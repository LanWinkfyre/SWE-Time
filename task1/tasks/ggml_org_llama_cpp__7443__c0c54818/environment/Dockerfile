# ggml-org/llama.cpp cut at fcf6538ba6702c55eaec70da9a75c81d04900a72: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e402de364b643cb89ea9f43057733b5d36298670 \
        --stage baseline --out /opt/swe-time/receipt.json
