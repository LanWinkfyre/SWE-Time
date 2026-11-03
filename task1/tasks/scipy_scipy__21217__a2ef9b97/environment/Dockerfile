# scipy/scipy cut at d60b48d0a457c1d92f4ad1b3e4ef5063ba170980: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe afeab37e1a02a0cf09d9507fddab05795eea14fa \
        --stage baseline --out /opt/swe-time/receipt.json
