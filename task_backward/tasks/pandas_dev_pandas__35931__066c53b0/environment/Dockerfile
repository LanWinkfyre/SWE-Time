# pandas-dev/pandas cut at e3bcf8d1949833793ff50cca393240dab0f0d461: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a1f605697e44e7668b64841baf4ab2988470d08c \
        --stage baseline --out /opt/swe-time/receipt.json
