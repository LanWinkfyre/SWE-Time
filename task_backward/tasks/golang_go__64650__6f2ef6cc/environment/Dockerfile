# golang/go cut at ba7c4e47b32fa99db8aa05331426b328bb39517a: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 59275e266a222564fc1a39f17b913a74838478f4 \
        --stage baseline --out /opt/swe-time/receipt.json
