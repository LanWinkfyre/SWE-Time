# curl/curl cut at ba7b94b1e74745eb8900ca4cccdec47473fc78f3: full history up to the cutoff, nothing after it.
# rebuild/rebuild.py places the repository in ./repo next to this file, so the build context is
# this environment/ directory.  Dockerfile.dockerignore is intentionally empty.
FROM swe-time/base:1
COPY repo /testbed/repo
RUN git config --global --add safe.directory /testbed/repo \
 && python3 /opt/swe-time/probe.py --repo /testbed/repo --future-probe 4298b97020020819d474f7aee372d68638145dc0 \
        --stage baseline --out /opt/swe-time/receipt.json
