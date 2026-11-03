# rust-lang/rust cut at f2d69d5a7c04617d122facd0a7a5bdde0af928ae: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6650252439d4e03368b305c42a10006e36f1545e \
        --stage baseline --out /opt/swe-time/receipt.json
