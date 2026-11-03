# darktable-org/darktable cut at 76cf661582f38e518e29a1b44ffce93865151917: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ecb3bd2f268df9971cc9a61cf88a493f86240a36 \
        --stage baseline --out /opt/swe-time/receipt.json
