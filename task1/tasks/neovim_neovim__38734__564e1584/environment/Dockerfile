# neovim/neovim cut at 333e3178eca0760019b1a759f67ac0b96cab50bd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 33b9a9dcf189369290e3bb6d195efb2394d485b9 \
        --stage baseline --out /opt/swe-time/receipt.json
