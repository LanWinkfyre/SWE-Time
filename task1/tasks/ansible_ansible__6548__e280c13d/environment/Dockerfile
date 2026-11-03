# ansible/ansible cut at 84908a57fce3e6c1919ab7b85839f40d7f7d9585: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe db3d2e1042c2ac60a899ccc745f579c364ff578a \
        --stage baseline --out /opt/swe-time/receipt.json
