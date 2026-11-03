# rails/rails cut at 474ebc55bd13ad58626a49dfc44c8e6407813935: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 11e8badb16876e6bd72c874631d25aec41dad293 \
        --stage baseline --out /opt/swe-time/receipt.json
