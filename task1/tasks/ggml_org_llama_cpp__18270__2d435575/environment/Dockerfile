# ggml-org/llama.cpp cut at e1f15b454fbadfddf8f1ec450bf6d390d9db7adb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 147a5216363c5b2edcdeb17f01ef3b28372ec872 \
        --stage baseline --out /opt/swe-time/receipt.json
