# godotengine/godot cut at 0586524b9ce67bdcab5cef88397c44bb7b9e46fb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b7d98d4d058388d7eb861abe4aed93c5a9480cf0 \
        --stage baseline --out /opt/swe-time/receipt.json
