# godotengine/godot cut at 955ed0a95f61e14e6c941540b11905a16fb40d00: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 85f4f3927973fa7b106ee274033b1f0180ad4343 \
        --stage baseline --out /opt/swe-time/receipt.json
