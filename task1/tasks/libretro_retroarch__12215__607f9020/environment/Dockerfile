# libretro/RetroArch cut at 21b2ec6bd528a6acc9fc145af9b057ad27213135: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 93174dcd19da168615e91fe26cfb57e8aeb9a049 \
        --stage baseline --out /opt/swe-time/receipt.json
