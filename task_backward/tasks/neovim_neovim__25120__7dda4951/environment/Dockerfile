# neovim/neovim cut at bc67cf3ccdf935a0e2974fbbe5557a3d24931c54: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1f551e068f728ff38bd7fdcfa3a6daf362bab9da \
        --stage baseline --out /opt/swe-time/receipt.json
