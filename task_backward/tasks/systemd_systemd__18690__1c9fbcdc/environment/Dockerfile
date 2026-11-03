# systemd/systemd cut at 66e52d22210eeec86fd87bc4ff2cc0b107546750: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 1f3315b8bdbc9240f70f90373f2b9043f2087ac5 \
        --stage baseline --out /opt/swe-time/receipt.json
