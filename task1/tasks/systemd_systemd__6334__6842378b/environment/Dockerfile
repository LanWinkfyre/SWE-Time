# systemd/systemd cut at cd2d4c7f689cc02b5a592e9212b30e46c516b676: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 634735b56b82bdde3c67193ba7b470bab80fdcbd \
        --stage baseline --out /opt/swe-time/receipt.json
