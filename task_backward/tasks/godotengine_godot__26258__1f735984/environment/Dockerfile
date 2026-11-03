# godotengine/godot cut at 74d0ed2236b333d0a292e15b9c2a9380c2c122a1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 31656301b2cfe3710a1bfe8d636eb8206d31dd7b \
        --stage baseline --out /opt/swe-time/receipt.json
