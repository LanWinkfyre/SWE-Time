# numpy/numpy cut at 4178b5a731cd183563d53ed145e7dce278aa39f6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1461f1da00fc34082d7a2693deb35c1990fd1b41 \
        --stage baseline --out /opt/swe-time/receipt.json
