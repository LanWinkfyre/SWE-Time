# godotengine/godot cut at bc7178422e98c86c7c8c9d9e572a9c6941836d79: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe db3dd67d47ed7d4aa8e0c652a9dfe836c568cf39 \
        --stage baseline --out /opt/swe-time/receipt.json
