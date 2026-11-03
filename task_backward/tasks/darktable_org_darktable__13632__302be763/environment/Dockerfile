# darktable-org/darktable cut at 4be1794967b781942a8bb3abf3b1cd331bddbed4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe df71c33c7c45bb3c4d52bf6e2d1dfefb7e94a49a \
        --stage baseline --out /opt/swe-time/receipt.json
