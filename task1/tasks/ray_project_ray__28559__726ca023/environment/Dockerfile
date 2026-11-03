# ray-project/ray cut at 86c552021b015aa0a0688b63ea5ee9a0487b0e11: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 8840be1942a69b2595a05c5c5556b0daec7abbcd \
        --stage baseline --out /opt/swe-time/receipt.json
