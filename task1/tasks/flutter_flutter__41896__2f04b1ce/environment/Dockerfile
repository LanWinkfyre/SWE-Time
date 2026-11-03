# flutter/flutter cut at fa7340a328cbfbe745748cfcd5d5fe08c401c64c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 439dc5cffef5530105e8cdb93eea32b2edc62f0a \
        --stage baseline --out /opt/swe-time/receipt.json
