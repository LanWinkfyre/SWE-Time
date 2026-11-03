# dart-lang/sdk cut at 69afe5a40710f45e7d7a5d749ff31fc30832ed08: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe ceaed93e3bb5688550343d1b7b07c282509ad80d \
        --stage baseline --out /opt/swe-time/receipt.json
