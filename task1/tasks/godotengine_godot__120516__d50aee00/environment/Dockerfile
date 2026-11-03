# godotengine/godot cut at f964fa714f503bd063b96f6194eb3e45355c1084: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cb4b6883cb79a9b5a6fd42b7c2118ce9515f7722 \
        --stage baseline --out /opt/swe-time/receipt.json
