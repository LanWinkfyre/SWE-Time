# microsoft/vscode cut at bef0623eddb2910095757a30fd77fb7ebcce4c93: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ebe6e7f4f23370f492bbcc660b7742ebec7f1ccb \
        --stage baseline --out /opt/swe-time/receipt.json
