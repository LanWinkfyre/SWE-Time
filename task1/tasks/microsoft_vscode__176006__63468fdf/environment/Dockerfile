# microsoft/vscode cut at 8354eaa91c05d25dd79da068e8a57b6849a24461: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 06ce7933733b1ab05e410e46a6a622dfffb31927 \
        --stage baseline --out /opt/swe-time/receipt.json
