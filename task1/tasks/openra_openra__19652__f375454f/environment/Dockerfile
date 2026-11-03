# OpenRA/OpenRA cut at e0e219793ff7b39bdec98b45fe9f0785d0612956: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 0b75991fbcd1cdca331235d554ca639226fd69d6 \
        --stage baseline --out /opt/swe-time/receipt.json
