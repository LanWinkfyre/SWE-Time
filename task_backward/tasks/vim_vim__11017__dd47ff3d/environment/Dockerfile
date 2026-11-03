# vim/vim cut at f240395fca63d4b330112a4b81e94b05b50de1aa: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 04c4c5746e15884768d2cb41370c3276a196cd4c \
        --stage baseline --out /opt/swe-time/receipt.json
