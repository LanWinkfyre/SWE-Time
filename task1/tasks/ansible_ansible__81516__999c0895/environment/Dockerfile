# ansible/ansible cut at bd3ffbe10903125993d7d68fa8cfd687124a241f: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0cba3b7504c1aabe0fc3773e3ff3ac024edeb308 \
        --stage baseline --out /opt/swe-time/receipt.json
