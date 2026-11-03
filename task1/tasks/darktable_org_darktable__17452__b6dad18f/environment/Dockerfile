# darktable-org/darktable cut at 83b4de58f0e8d4ecec0a1079bad72a357ef7f10a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e5cafa1ec128c9c2171329c7415fe957e298664c \
        --stage baseline --out /opt/swe-time/receipt.json
