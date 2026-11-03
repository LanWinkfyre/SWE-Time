# vim/vim cut at cce81e9673fe8d056e8eef310d9919620eccb2f2: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 826bfe4bbd7594188e3d74d2539d9707b1c6a14b \
        --stage baseline --out /opt/swe-time/receipt.json
