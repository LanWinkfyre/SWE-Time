# microsoft/TypeScript cut at a05b7ec01fc9f1a8001e4556b56a151246b75f2c: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6860373c1a15888199e6613552bbdbc2c79f703a \
        --stage baseline --out /opt/swe-time/receipt.json
