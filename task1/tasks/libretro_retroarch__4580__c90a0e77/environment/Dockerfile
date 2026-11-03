# libretro/RetroArch cut at 74d29c4b40fff7e6afc5e0258f79294bd68fbaa6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e05a8a7460245f93dd3a975400e2a4b7f85a401d \
        --stage baseline --out /opt/swe-time/receipt.json
