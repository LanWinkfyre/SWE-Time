# vim/vim cut at 1ac90b4fa63414d56750559506a3e076df6923b0: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe a046b37c22bcabdea5f0fd6d21ca4bd0aa4c768e \
        --stage baseline --out /opt/swe-time/receipt.json
