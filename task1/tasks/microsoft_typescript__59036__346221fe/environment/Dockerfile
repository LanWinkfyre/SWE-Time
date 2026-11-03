# microsoft/TypeScript cut at ef339af12801c1f88ff4e01d4d4e602addfcca98: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 15f67e0b482faf9f6a3ab9965f3c11196bf3e99b \
        --stage baseline --out /opt/swe-time/receipt.json
