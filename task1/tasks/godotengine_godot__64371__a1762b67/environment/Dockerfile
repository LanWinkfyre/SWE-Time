# godotengine/godot cut at f2a61684143af02a8cbe7002645af817607f9bd6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 128d68796d9f412a5b05cca8714f217341cfa376 \
        --stage baseline --out /opt/swe-time/receipt.json
