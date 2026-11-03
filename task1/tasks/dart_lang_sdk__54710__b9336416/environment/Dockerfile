# dart-lang/sdk cut at ba8b4704e94035fb7e10c520c0a504dc8010765d: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 7f6b082216cb894b8e237b174f5fc8976126d9e3 \
        --stage baseline --out /opt/swe-time/receipt.json
