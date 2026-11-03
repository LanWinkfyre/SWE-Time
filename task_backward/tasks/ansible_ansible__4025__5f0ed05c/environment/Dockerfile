# ansible/ansible cut at fff497a1aef6db7f2a8f92d981a6b9a789bf798e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7e849ac7e06adfe19b34934e54ac02aa450fbe24 \
        --stage baseline --out /opt/swe-time/receipt.json
