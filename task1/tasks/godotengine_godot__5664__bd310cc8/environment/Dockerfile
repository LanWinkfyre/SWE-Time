# godotengine/godot cut at 5545afd52b912722bbdb6e412cce9593857c5726: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1403fa18a9cf1077d9b7ec974ee9f77249ae49b6 \
        --stage baseline --out /opt/swe-time/receipt.json
