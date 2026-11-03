# ansible/ansible cut at b97887ba4103acbacda7a99b3115a5a112788a51: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7ba4f5ee12683f3e1376eb11e5646209f51233c7 \
        --stage baseline --out /opt/swe-time/receipt.json
