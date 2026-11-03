# JuliaLang/julia cut at f6e2b989de8ba14d9356ef065497fab8e20d66a6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e331deb8672117845c5848aec0712d5a5cd0d389 \
        --stage baseline --out /opt/swe-time/receipt.json
