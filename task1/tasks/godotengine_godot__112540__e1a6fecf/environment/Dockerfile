# godotengine/godot cut at 6fd949a6dcbda94140200633394f2b4b99de8f6f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4c5f6691f083c8defae21f85c9287da8e4a05afd \
        --stage baseline --out /opt/swe-time/receipt.json
