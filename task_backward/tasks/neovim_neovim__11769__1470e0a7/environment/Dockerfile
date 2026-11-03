# neovim/neovim cut at 6f073ccbf464e2f2cd6d6855aa3f27ee1adcc20d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 9dc3247850d057bca3250f26ca8d0578d6b35455 \
        --stage baseline --out /opt/swe-time/receipt.json
