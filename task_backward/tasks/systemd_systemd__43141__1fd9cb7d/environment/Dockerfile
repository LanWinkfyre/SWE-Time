# systemd/systemd cut at 7cc277fb97172d11daf16d8b1b185ca743d1d73c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c844a88f69aa4a24c5a3a591e51e9ba3488002cf \
        --stage baseline --out /opt/swe-time/receipt.json
