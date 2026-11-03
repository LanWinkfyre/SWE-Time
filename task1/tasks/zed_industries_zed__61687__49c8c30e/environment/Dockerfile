# zed-industries/zed cut at c214057e086517920b214800725c5d16294ddf0d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe afd17238ed257d4b7130891e339c534c1a9a828a \
        --stage baseline --out /opt/swe-time/receipt.json
