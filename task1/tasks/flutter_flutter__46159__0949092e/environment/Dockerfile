# flutter/flutter cut at 649e188562e45338daef56e336620a6f13e73ad5: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 99684ce1599170219667a912332317e358f7f05f \
        --stage baseline --out /opt/swe-time/receipt.json
