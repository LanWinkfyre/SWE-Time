# dart-lang/sdk cut at 47f7c4fb8731394e8843478d68518de1db92eaca: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 87575b2578aa729b83842261e452645cfb08e24e \
        --stage baseline --out /opt/swe-time/receipt.json
