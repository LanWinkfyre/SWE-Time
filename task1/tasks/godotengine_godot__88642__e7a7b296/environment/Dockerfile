# godotengine/godot cut at 16d61427cab3a8e43f0a9a8ee724fc176b6433c6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e8758a0b5e9616e20a5a4a4591b8aa1561f44a9f \
        --stage baseline --out /opt/swe-time/receipt.json
