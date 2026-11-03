# darktable-org/darktable cut at 11f26a81c48bd3f38f65a4b6819b3aaf02ee6f71: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0091f2de91c52d5d1dbf083b67fc5ad156a549f2 \
        --stage baseline --out /opt/swe-time/receipt.json
