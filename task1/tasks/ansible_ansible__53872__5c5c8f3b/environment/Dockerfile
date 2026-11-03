# ansible/ansible cut at 906427cabac133d3690aff2225d33ef0dd34bcd5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 387bb0adfe00784e44f4693768360a9eb806e790 \
        --stage baseline --out /opt/swe-time/receipt.json
