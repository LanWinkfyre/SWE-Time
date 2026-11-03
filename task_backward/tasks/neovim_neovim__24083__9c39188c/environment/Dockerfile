# neovim/neovim cut at 8d4a53fe6e20652946948170f2436ec520f9bdfe: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ded01a819ab0e10104aa29ab67cf67e4efd75e04 \
        --stage baseline --out /opt/swe-time/receipt.json
