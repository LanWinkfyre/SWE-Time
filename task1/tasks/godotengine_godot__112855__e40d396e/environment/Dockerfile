# godotengine/godot cut at ef34c3d534a16b140aef0643ed2fa36f8e9d1612: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 359ef8fc2b771b8cde320a8eb443220fe635c89d \
        --stage baseline --out /opt/swe-time/receipt.json
