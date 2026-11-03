# llvm/llvm-project cut at 803b79221edfc2517e6bfc373e5f55609565b0e4: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3f0df4d7b0269623cfcd0ef6272e6a3a2ad9066d \
        --stage baseline --out /opt/swe-time/receipt.json
