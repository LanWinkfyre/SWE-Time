# neovim/neovim cut at 83b6d9f197a44e3b8140619e6b7e9950f217aafb: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe efaf4732e26e2f0fbfab947296141376223b30d7 \
        --stage baseline --out /opt/swe-time/receipt.json
