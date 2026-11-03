# godotengine/godot cut at 51105ccbe58381774ecd7a7486d564b202a5192e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 81b7ccaed3a243b718b37ee2786fa3bac87e3204 \
        --stage baseline --out /opt/swe-time/receipt.json
