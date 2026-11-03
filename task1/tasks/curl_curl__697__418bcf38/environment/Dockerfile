# curl/curl cut at 3c2ef2a610814028a8dc9469b350d291327c673f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 33a0a926c59cd848f20764ecf0144f69df576c68 \
        --stage baseline --out /opt/swe-time/receipt.json
