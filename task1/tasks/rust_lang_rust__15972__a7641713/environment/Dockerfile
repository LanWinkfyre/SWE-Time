# rust-lang/rust cut at 4e388859a2e12f4019a09224d626eb07b8333651: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e5984640e63d2e9f613d857ad2d48ff57b310655 \
        --stage baseline --out /opt/swe-time/receipt.json
