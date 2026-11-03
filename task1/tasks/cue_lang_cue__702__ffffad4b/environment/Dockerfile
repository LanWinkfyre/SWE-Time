# cue-lang/cue cut at 06484a39d8d44c656212ac2d3b5589f8aa9db033: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 6da50d98f650ded66f7b4ad8cda565e928dfaae0 \
        --stage baseline --out /opt/swe-time/receipt.json
