# darktable-org/darktable cut at 0930cccd42d3cc94e04345da5a6779d1ebdaaeff: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ee79b28f8468692f2117ace33caf95d0f7361f52 \
        --stage baseline --out /opt/swe-time/receipt.json
