# golang/go cut at 3c1b7bc7212cd894dae684ae064f4e7708b080ec: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2524ed19946f10a9b0ecc4bf54f1a23c18faa525 \
        --stage baseline --out /opt/swe-time/receipt.json
