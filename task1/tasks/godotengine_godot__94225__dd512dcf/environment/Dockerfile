# godotengine/godot cut at 383a6e4ef285fddcb0e1cbe28a20332c7e5a815b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b6434f2ac7a1c22c057cc28022fce6e7b965536d \
        --stage baseline --out /opt/swe-time/receipt.json
