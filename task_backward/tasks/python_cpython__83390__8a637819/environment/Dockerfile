# python/cpython cut at 7dc72b8d4f2c9d1eed20f314fd6425eab66cbc89: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ec007cb43faf5f33d06efbc28152c7fdcb2edb9c \
        --stage baseline --out /opt/swe-time/receipt.json
