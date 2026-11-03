# neovim/neovim cut at 3fbff98cfd48941ceac086543dd7d6bcdbfb18ab: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 399b47fddbd942cc32ebcf9e08799c9544b4d5fe \
        --stage baseline --out /opt/swe-time/receipt.json
