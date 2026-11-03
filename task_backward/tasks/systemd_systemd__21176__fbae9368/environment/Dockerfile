# systemd/systemd cut at ff8b7bd6a0d15311889103c49f752b03d4d830a3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d36a343c52967a89926b3b0e525105382331dfba \
        --stage baseline --out /opt/swe-time/receipt.json
