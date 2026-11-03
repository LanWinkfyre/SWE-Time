# ansible/ansible cut at f0f20d8a1c593005627250f17c0401df13ac26c0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 952e842720cbe4b537bdc61238c30da94f0c4dd3 \
        --stage baseline --out /opt/swe-time/receipt.json
