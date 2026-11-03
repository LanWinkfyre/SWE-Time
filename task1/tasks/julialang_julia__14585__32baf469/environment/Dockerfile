# JuliaLang/julia cut at bc1c18ec2f3452de4b5cb714191478e02bb3847a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe bade595c1eb60dda318a7ae8356b7338a315d2f6 \
        --stage baseline --out /opt/swe-time/receipt.json
