# vim/vim cut at f562e72df726c6191fa305e1c0a113f1cfb87f76: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 72ab729c3dcdea0fba44d8e676602c847e841bcd \
        --stage baseline --out /opt/swe-time/receipt.json
