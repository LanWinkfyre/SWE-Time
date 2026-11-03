# python/cpython cut at 8feb7ab77c80968a6de6079299a39b0494b1701b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a0bc75e2fdd53680cb147881bcb3754bd56aa2fa \
        --stage baseline --out /opt/swe-time/receipt.json
