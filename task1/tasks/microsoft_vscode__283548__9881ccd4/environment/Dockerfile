# microsoft/vscode cut at a7cfff7ea03e94f9dade0742980de36fc56848a1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e5b4dd5eb043b1be37cb44ae27e1e0d17aa146da \
        --stage baseline --out /opt/swe-time/receipt.json
