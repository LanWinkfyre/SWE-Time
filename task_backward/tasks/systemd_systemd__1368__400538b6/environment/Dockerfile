# systemd/systemd cut at 56c581598389739ba2a97baf896ea9277c278a1d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2e396de8b2317fdd1cb2f5eb1df8dffd13bf1e80 \
        --stage baseline --out /opt/swe-time/receipt.json
