# rust-lang/rust cut at 14196dbfa3eb7c30195251eac092b1b86c8a2d84: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a72e2a71d8fbcbc46cdd18784e2ab2c32cbd9c93 \
        --stage baseline --out /opt/swe-time/receipt.json
