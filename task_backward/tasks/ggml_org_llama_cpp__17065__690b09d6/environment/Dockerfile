# ggml-org/llama.cpp cut at 7f09a680af6e0ef612de81018e1d19c19b8651e8: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5c9a18e674be444e847d8e07a6b851764708fb12 \
        --stage baseline --out /opt/swe-time/receipt.json
