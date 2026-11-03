# JuliaLang/julia cut at c9c281e7938df9c5ec82ea6758966755fabb7127: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 92af1bbfb934d89fb4772c05b422da6236377a50 \
        --stage baseline --out /opt/swe-time/receipt.json
