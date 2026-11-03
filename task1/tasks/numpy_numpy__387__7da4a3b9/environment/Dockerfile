# numpy/numpy cut at 63cd8f3cc751771fd27636009b8c0341a2beff45: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 5c944b9c6915264380aa2df3dcfd0629867fbe80 \
        --stage baseline --out /opt/swe-time/receipt.json
