# curl/curl cut at 5bae72734b45a01c6337eb3b2c40020c4e904415: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ce0881edee3c78609eae49665fb70264d8786d29 \
        --stage baseline --out /opt/swe-time/receipt.json
