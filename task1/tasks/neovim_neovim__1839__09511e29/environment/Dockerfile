# neovim/neovim cut at bff48b23d700d6202e1c85564cd7fcb1b3ce4c34: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c7f4e553629f9ac667dee1e920b96c7c327380f6 \
        --stage baseline --out /opt/swe-time/receipt.json
