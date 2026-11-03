# ansible/ansible cut at 7f41f0168a7219e825711ffba853478187c26ab6: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe aef16ee1956e8383358697e5356853308af9b7b3 \
        --stage baseline --out /opt/swe-time/receipt.json
