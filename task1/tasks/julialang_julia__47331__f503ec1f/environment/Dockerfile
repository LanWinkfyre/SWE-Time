# JuliaLang/julia cut at 48abb7206d243decca0c4e93eb71db613cd5032b: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7cbf55f4677d243629e685348726ab4941a50706 \
        --stage baseline --out /opt/swe-time/receipt.json
