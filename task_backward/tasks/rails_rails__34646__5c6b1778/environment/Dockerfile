# rails/rails cut at b86f65a816546ff8eea39d25b62c995c7efc21dc: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe f173ec77fc35ce57e94398310308e868689366bb \
        --stage baseline --out /opt/swe-time/receipt.json
