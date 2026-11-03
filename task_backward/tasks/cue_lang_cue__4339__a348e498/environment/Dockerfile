# cue-lang/cue cut at 35cefbf9b4880261ad6dcdecce7c7e44a79a313c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7efad27a0ba82934599c6fdba5794f8d2e8eb916 \
        --stage baseline --out /opt/swe-time/receipt.json
