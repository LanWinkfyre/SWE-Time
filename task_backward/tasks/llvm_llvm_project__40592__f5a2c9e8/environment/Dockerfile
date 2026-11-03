# llvm/llvm-project cut at 982726ea010fda10ecb87a851ed08a2df740c05b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 55d495475c955384fdc0c4a18b5670ed8b1dedcf \
        --stage baseline --out /opt/swe-time/receipt.json
