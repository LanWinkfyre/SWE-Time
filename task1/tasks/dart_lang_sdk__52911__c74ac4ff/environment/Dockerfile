# dart-lang/sdk cut at 86d1261dff279acf84bc699c6c116189955b0076: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4333288aaa3de000ee38fcaa0d051cef41c300e4 \
        --stage baseline --out /opt/swe-time/receipt.json
