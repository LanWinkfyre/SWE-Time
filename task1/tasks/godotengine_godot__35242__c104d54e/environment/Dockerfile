# godotengine/godot cut at e7ee9e01a64bb1296431d82f9f1d888a90b6ea1c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c6f0c0d12e3175ef0a60d8b6f5922bb314b66bf0 \
        --stage baseline --out /opt/swe-time/receipt.json
