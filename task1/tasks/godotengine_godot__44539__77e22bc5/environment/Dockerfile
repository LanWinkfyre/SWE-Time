# godotengine/godot cut at e9d12f9e4ea30a6c3f2cf179f104a153d668c2a3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bc2ac0bbd685a01569ba6dde4c68adc1ccf37bb8 \
        --stage baseline --out /opt/swe-time/receipt.json
