# godotengine/godot cut at 7c7a86f0fd0c1ae94099f2c1fdd878ab60dcb077: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 56563ef09e779b9f4b105fea0e5a1a8e59c7cfe8 \
        --stage baseline --out /opt/swe-time/receipt.json
