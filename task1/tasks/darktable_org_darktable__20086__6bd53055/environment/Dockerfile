# darktable-org/darktable cut at 65fe2e9e3ae0726fb6756e185df27b0b46b12e61: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2232d1220627ff134b00b4993047ae732240fa4b \
        --stage baseline --out /opt/swe-time/receipt.json
