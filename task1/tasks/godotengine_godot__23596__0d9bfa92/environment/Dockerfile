# godotengine/godot cut at 43e358205831fbcc5d6d7e8aade5131168d83651: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d403b4086c514647bba7620591061b7de7dfaf4b \
        --stage baseline --out /opt/swe-time/receipt.json
