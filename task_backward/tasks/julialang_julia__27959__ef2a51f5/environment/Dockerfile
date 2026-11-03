# JuliaLang/julia cut at feaee9ebbc22b04d1fe9a4fbe74e36c317b71046: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a2f0a30ef6d341a2f513e3744fff2f6d4155c249 \
        --stage baseline --out /opt/swe-time/receipt.json
