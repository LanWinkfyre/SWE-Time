# rust-lang/rust cut at 532d2b14c05f9bc20b2d27cbb5f4550d28343a36: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 14c1e71d095a5500def51d4e405bd2b0010f3d37 \
        --stage baseline --out /opt/swe-time/receipt.json
