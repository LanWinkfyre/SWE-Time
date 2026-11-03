# godotengine/godot cut at b19c9bd1983b8c72621595b7c22daade4ebf6625: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe b87a232668d9f9f3b32c2fceb60bc5f6ef46df22 \
        --stage baseline --out /opt/swe-time/receipt.json
