# rust-lang/rust cut at d49994b060684af423339b55769439b2f444a7b9: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 2c243d957008f5909f7a4af19e486ea8a3814be7 \
        --stage baseline --out /opt/swe-time/receipt.json
