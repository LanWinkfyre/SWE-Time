# dart-lang/sdk cut at 57d256377c7ec99ada943cd2c8e5855557ea2405: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4d271519a18adcb06b11842ec3f6e3c1b576b531 \
        --stage baseline --out /opt/swe-time/receipt.json
