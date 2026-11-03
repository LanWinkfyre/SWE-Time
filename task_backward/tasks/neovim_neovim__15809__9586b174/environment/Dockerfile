# neovim/neovim cut at bec7f47cee8b69fbaa3452762745c9d0e8ea4256: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 96614f84abb43ad2e6b610dfbbda4d075a2a0aad \
        --stage baseline --out /opt/swe-time/receipt.json
