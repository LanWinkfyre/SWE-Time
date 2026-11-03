# scipy/scipy cut at 7d936fa25e2e8fa74ec6399620dd6490e4dfb33e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c20c693f7a3e4819d258c68a8b69f660aefac6b1 \
        --stage baseline --out /opt/swe-time/receipt.json
