# neovim/neovim cut at 6af64d384f96a69462a2a50dd7054566af98de37: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe d956842751aaf88656825b236c27020596d96b6a \
        --stage baseline --out /opt/swe-time/receipt.json
