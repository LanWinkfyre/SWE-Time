# darktable-org/darktable cut at 54e7e09eb172aa76faa870afbf238c45d7b77b96: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3ce77d9b34b55d0076d6019e4ac131be88879d28 \
        --stage baseline --out /opt/swe-time/receipt.json
