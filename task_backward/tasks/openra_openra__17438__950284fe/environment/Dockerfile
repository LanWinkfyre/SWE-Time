# OpenRA/OpenRA cut at 22374ed73263cdaea71f4576476caa147b02dffe: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5afc1c144386ffa64296ff853c8d17733bf48b2a \
        --stage baseline --out /opt/swe-time/receipt.json
