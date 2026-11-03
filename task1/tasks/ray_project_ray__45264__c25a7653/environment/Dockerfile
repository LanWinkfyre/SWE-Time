# ray-project/ray cut at a3d5874c9e0b1198aa2ed7e2fbbb0a29a57b3a14: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 795c3239fb3f46f3ab593dc01f0eafc985dd4eda \
        --stage baseline --out /opt/swe-time/receipt.json
