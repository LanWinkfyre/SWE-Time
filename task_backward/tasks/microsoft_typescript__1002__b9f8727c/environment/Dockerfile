# microsoft/TypeScript cut at 5ce3baf339e0424263069c70f0ea239bc3cea96a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ddc08ba4679cfc8687dd8dd0da21d7f62e93d4f4 \
        --stage baseline --out /opt/swe-time/receipt.json
