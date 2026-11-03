# llvm/llvm-project cut at cc613052fd6afe2e3522c18234e382588069441d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 86d7405f428e0cf4cdeba55babbcd111ab499370 \
        --stage baseline --out /opt/swe-time/receipt.json
