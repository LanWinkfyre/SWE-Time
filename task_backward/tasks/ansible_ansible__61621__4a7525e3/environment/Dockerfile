# ansible/ansible cut at 0e1ec04efb10590a99bf7d6f30b2af6731a8239e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 35359959de04d6848e437ac186645acaf78fa2e8 \
        --stage baseline --out /opt/swe-time/receipt.json
