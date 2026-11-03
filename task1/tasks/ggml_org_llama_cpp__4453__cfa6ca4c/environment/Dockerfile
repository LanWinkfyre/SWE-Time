# ggml-org/llama.cpp cut at 948ff137ec37f1ec74c02905917fa0afc9b97514: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0353a1840134b24b07ab61fd4490192f28c4db6b \
        --stage baseline --out /opt/swe-time/receipt.json
