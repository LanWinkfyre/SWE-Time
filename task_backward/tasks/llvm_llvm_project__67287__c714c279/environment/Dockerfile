# llvm/llvm-project cut at 24e33b594503f0283d31b89e2694e3d798def5ac: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e5038f0f34c93399ee99e31c739f9945cadf9b70 \
        --stage baseline --out /opt/swe-time/receipt.json
