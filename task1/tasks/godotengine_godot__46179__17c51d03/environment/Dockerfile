# godotengine/godot cut at 5c2fe970b87f8e95306bad0f713567a150b1e442: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7eb4e6415d74e3d4dae6ddd12bb0bdb7acf221c0 \
        --stage baseline --out /opt/swe-time/receipt.json
