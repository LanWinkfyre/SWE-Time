# curl/curl cut at f72b84809216657e4ad3c1a0184775c911080d63: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cbf8fecda5fd70d3f5b183a43416e75dc6dad7ea \
        --stage baseline --out /opt/swe-time/receipt.json
