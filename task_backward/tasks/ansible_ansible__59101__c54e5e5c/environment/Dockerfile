# ansible/ansible cut at 262c9ffdb6c995d67a8dfd3707ec8bb09a4fd77d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 30206d30660a2f1d21482ae55aa530d40c776cfc \
        --stage baseline --out /opt/swe-time/receipt.json
