# libretro/RetroArch cut at 45764673c76fca3a95b8c4f3f4c4866051c545e7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe cc57bbc06e87cb6770d83345e760d20df6ecb5cd \
        --stage baseline --out /opt/swe-time/receipt.json
