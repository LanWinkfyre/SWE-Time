# microsoft/vscode cut at a28eab68734e629c61590fae8c4b231c91f0eaaa: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 98d9782b8bc77891135a5b295c9489e7ddf0d2a4 \
        --stage baseline --out /opt/swe-time/receipt.json
