# libretro/RetroArch cut at 861d87281ee075eb811f77ad83d6115c396763e1: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe e4476ec61b13635019f138ed192c54d267657695 \
        --stage baseline --out /opt/swe-time/receipt.json
