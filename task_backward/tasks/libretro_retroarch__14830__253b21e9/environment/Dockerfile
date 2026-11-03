# libretro/RetroArch cut at e10361ed529cd07651012f0437911e7f5d9f2bdd: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 975300a3208a2deca599a7d55c74a86e159fb45b \
        --stage baseline --out /opt/swe-time/receipt.json
