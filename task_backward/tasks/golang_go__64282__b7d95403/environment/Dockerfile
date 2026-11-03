# golang/go cut at 468bc941886ae83b8d16af5deaaf12ea5cabb05b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0709f1bb00287371da61a1fc94f6e2a086aa0f29 \
        --stage baseline --out /opt/swe-time/receipt.json
