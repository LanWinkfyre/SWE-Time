# neovim/neovim cut at 39ad99b594aa68b6c3024dd9bfa3f7e31c14dff9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6fe9a12268c9e7d23f03f9fb1841c9bfebdb1bf3 \
        --stage baseline --out /opt/swe-time/receipt.json
