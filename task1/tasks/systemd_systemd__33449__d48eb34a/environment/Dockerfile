# systemd/systemd cut at eb37c0c07809d48aba34ffeced5c18055b70d81e: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 59a7019fee57b36a3deb470af09c0573de6f4a47 \
        --stage baseline --out /opt/swe-time/receipt.json
