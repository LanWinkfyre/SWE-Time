# ansible/ansible cut at 347aa7b0328699b33cf8d435511b42285bf87da7: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe c022a43a47eee8debe3d026d571a419d9c8c2eda \
        --stage baseline --out /opt/swe-time/receipt.json
