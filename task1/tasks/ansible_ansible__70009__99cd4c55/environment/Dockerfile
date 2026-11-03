# ansible/ansible cut at ebb22655e42f944cfa898488a7cfd3003297ecfe: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4869874337bcb68154f8c29db12cfcd3d7281892 \
        --stage baseline --out /opt/swe-time/receipt.json
