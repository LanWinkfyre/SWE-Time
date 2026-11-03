# mpv-player/mpv cut at 48e6c35c0e056d9e4ff04b98e012416697736d8a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7f72f64b7f9a00c5f71bf975f11d7929ac8e087f \
        --stage baseline --out /opt/swe-time/receipt.json
