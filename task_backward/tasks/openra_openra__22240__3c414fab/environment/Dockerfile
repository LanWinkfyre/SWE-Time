# OpenRA/OpenRA cut at c588c3ef8dd108677a5c3143cbd0810bb5969608: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 962e7e911d0cc908eec02944aa72c0b08e0e8338 \
        --stage baseline --out /opt/swe-time/receipt.json
