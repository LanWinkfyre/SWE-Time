# neovim/neovim cut at 21a0227d2f654ddc568c3733e72150021cd84a6b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6303d3680c7f76e8da732376e44e8b0c95520977 \
        --stage baseline --out /opt/swe-time/receipt.json
