# ansible/ansible cut at 69c9fbed26543bb3a998c2b0d0a76db05358febf: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 3d26431e4f9b2bada9307b3943a5179fc41f074a \
        --stage baseline --out /opt/swe-time/receipt.json
