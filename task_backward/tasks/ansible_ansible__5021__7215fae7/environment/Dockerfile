# ansible/ansible cut at 815b32685b377a9cc07c7a6f06bb080025b174fe: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e54a574bb292973442694abd73c16254042fdb29 \
        --stage baseline --out /opt/swe-time/receipt.json
