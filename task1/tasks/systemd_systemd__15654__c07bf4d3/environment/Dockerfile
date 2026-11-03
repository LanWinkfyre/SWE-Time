# systemd/systemd cut at 9dcd43b14927fe6f9182a252213dbf182d9d8e01: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe db72aea4a952cdfdef51eda03408d7c4a11e7359 \
        --stage baseline --out /opt/swe-time/receipt.json
