# openssl/openssl cut at 62f27ab9dcf29876b15cdae704c3a04b4c8a6344: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 993c437dbd14579cbbd55a2742274f10fc7c6e21 \
        --stage baseline --out /opt/swe-time/receipt.json
