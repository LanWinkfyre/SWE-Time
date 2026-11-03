# vim/vim cut at 218beb3e96bcb7b20395be3bec6076c767be71a1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3cb4448b8a5c0192988f4e349aba6d7a91a9a4bd \
        --stage baseline --out /opt/swe-time/receipt.json
