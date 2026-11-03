# numpy/numpy cut at 1a7e80f3d356ceb77f8c19ea326d1cdc79b73c9e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6031da18454335b7df95bed6597e95154bbdba2f \
        --stage baseline --out /opt/swe-time/receipt.json
