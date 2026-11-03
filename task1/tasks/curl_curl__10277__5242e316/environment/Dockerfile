# curl/curl cut at 5cf5bfcd134c1378af6dbae723abf88e309117df: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe db91dbbf2c0a853670ce0246d6d6579e6b0f6c0c \
        --stage baseline --out /opt/swe-time/receipt.json
