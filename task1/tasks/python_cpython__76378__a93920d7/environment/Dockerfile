# python/cpython cut at af5a895073c24637c094772b27526b94a12ec897: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 13badcbc60cdbfae1dba1683fd2fae9d70717143 \
        --stage baseline --out /opt/swe-time/receipt.json
