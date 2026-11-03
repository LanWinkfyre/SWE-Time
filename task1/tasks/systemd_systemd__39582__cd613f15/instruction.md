# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
systemd-tpm2-setup is flaky, fails in TEST-70-TPM2 and real systems

```
[  155.851313] TEST-70-TPM2.sh[3862]: + mkdir -p /run/nvpcr
[  155.852643] TEST-70-TPM2.sh[3862]: + cat
[  155.853863] TEST-70-TPM2.sh[3862]: + /usr/lib/systemd/systemd-tpm2-setup
[  155.856927] TEST-70-TPM2.sh[4007]: Loaded SRK public key from '/run/systemd/tpm2-srk-public-key.pem'.
[  155.859938] TEST-70-TPM2.sh[4007]: Loaded SRK public key fingerprint: f0a0e366fc6ce6fbaa6c7d0ea286c1e245327e0f6d32717791b7dc6d2629b29d
[  155.860293] TEST-70-TPM2.sh[4007]: Loaded SRK public key from '/var/lib/systemd/tpm2-srk-public-key.pem'.
[  155.860293] TEST-70-TPM2.sh[4007]: Loaded SRK public key fingerprint: f0a0e366fc6ce6fbaa6c7d0ea286c1e245327e0f6d32717791b7dc6d2629b29d
[  155.860963] TEST-70-TPM2.sh[4007]: Loaded 'libtss2-esys.so.0' via dlopen()
[  155.860963] TEST-70-TPM2.sh[4007]: Loaded 'libtss2-rc.so.0' via dlopen()
[  155.860963] TEST-70-TPM2.sh[4007]: Loaded 'libtss2-mu.so.0' via dlopen()
[  155.860963] TEST-70-TPM2.sh[4007]: Using TPM2 TCTI driver 'device' with device '/dev/tpmrm0'.
[  155.862461] TEST-70-TPM2.sh[4007]: Loaded 'libtss2-tcti-device.so.0' via dlopen()
[  155.862461] TEST-70-TPM2.sh[4007]: Loaded TCTI module 'tcti-device' (TCTI module for communication with Linux kernel interface.) [Version 2]
[  155.865162] TEST-70-TPM2.sh[4007]: TPM successfully started up.
[  155.865162] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0000 property 0x0001 count 127.
[  155.869382] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0002 property 0x011f count 256.
[  155.875917] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0008 property 0x0000 count 508.
[  155.878426] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0005 property 0x0000 count 1.
[  155.882847] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0001 property 0x81000001 count 1.
[  155.894110] TEST-70-TPM2.sh[4007]: SRK already stored in the TPM.
[  155.894396] TEST-70-TPM2.sh[4007]: SRK fingerprint is f0a0e366fc6ce6fbaa6c7d0ea286c1e245327e0f6d32717791b7dc6d2629b29d.
[  155.894396] TEST-70-TPM2.sh[4007]: SRK saved in '/var/lib/systemd/tpm2-srk-public-key.pem' matches SRK in TPM2.
[  155.895057] TEST-70-TPM2.sh[4007]: Using TPM2 TCTI driver 'device' with device '/dev/tpmrm0'.
[  155.895057] TEST-70-TPM2.sh[4007]: Loaded 'libtss2-tcti-device.so.0' via dlopen()
[  155.895057] TEST-70-TPM2.sh[4007]: Loaded TCTI module 'tcti-device' (TCTI module for communication with Linux kernel interface.) [Version 2]
[  155.898410] TEST-70-TPM2.sh[4007]: TPM successfully started up.
[  155.898410] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0000 property 0x0001 count 127.
[  155.902916] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0002 property 0x011f count 256.
[  155.910354] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0008 property 0x0000 count 508.
[  155.912659] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0005 property 0x0000 count 1.
[  155.916794] TEST-70-TPM2.sh[4007]: NvPCR 'cryptsetup' is already anchored.
[  155.917109] TEST-70-TPM2.sh[4007]: NvPCR 'hardware' is already anchored.
[  155.917109] TEST-70-TPM2.sh[4007]: Need anchor secret.
[  155.917837] TEST-70-TPM2.sh[4007]: Using TPM2 TCTI driver 'device' with device '/dev/tpmrm0'.
[  155.917837] TEST-70-TPM2.sh[4007]: Loaded 'libtss2-tcti-device.so.0' via dlopen()
[  155.917837] TEST-70-TPM2.sh[4007]: Loaded TCTI module 'tcti-device' (TCTI module for communication with Linux kernel interface.) [Version 2]
[  155.921232] TEST-70-TPM2.sh[4007]: TPM successfully started up.
[  155.921232] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0000 property 0x0001 count 127.
[  155.925941] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0002 property 0x011f count 256.
[  155.933519] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0008 property 0x0000 count 508.
[  155.935737] TEST-70-TPM2.sh[4007]: Getting TPM2 capability 0x0005 property 0x0000 count 1.
[  155.940094] TEST-70-TPM2.sh[4007]: Creating primary key on TPM.
[  155.955794] TEST-70-TPM2.sh[4007]: Successfully created primary key on TPM in 15ms.
[  155.956180] TEST-70-TPM2.sh[4007]: Loading HMAC key into TPM for shard 0.
[  155.956180] TEST-70-TPM2.sh[4007]: Loading object into TPM.
[  155.991510] TEST-70-TPM2.sh[4007]: Starting HMAC encryption session.
[  156.051823] TEST-70-TPM2.sh[4007]: Starting policy session.
[  156.133435] TEST-70-TPM2.sh[4007]: Building sealing policy.
[  156.133435] TEST-70-TPM2.sh[4007]: Reading PCR selection: [sha256(11)]
[  156.214095] TEST-70-TPM2.sh[4007]: Read PCR selection: [sha256(11)]
[  156.214095] TEST-70-TPM2.sh[4007]: PCR value: 11:sha256=e6e64991a7f168478898b7b060777e46fd81f30207828c702df171184e5462b7
[  156.214095] TEST-70-TPM2.sh[4007]: Adding PCR signature policy.
[  156.214095] TEST-70-TPM2.sh[4007]: Loading external key into TPM.
[  156.318305] TEST-70-TPM2.sh[4007]: Object name: 000b96ff8fe8fdb881c004299869b9336c1af410a63a60bbcb995f9d84c3d2501cc8
[  156.318305] TEST-70-TPM2.sh[4007]: Submitting PCR hash policy.
[  156.423078] TEST-70-TPM2.sh[4007]: Acquiring policy digest.
[  156.518625] TEST-70-TPM2.sh[4007]: Session policy digest: fde9362c534b37beb4e756b51902075076ea6aa3802af28af03964c8d5bb4fd7
[  156.518625] TEST-70-TPM2.sh[4007]: Couldn't find signature for this PCR bank, PCR index and public key.
[  156.826397] TEST-70-TPM2.sh[4007]: Failed to unseal secret using TPM2: No such device or address
[  156.826397] TEST-70-TPM2.sh[4007]: Failed to acquire anchor secret: No such device or address
```

https://github.com/systemd/systemd/actions/runs/19107312279/job/54594626863

[TEST-70-TPM2-1.journal.gz](https://github.com/user-attachments/files/23377200/TEST-70-TPM2-1.journal.gz)

I encounter the same error messages on my regular system using the current head, so I don't think this is a flaky test so much as an actual bug. I will try to bisect this when I have the time.
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `fea7f5d68b5a6272ce8989e872a57b42121b5205` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
