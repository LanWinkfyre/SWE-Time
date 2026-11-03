# Recover the symbolic verification state this change produces

A regression report was filed against `emmercm/igir`.  The report is quoted verbatim below.

## Report

```
Support No-Intro id/cloneofid parent/clone attributes

Hi, I cannot understand why the single option writes multiple files on certain parent/clones relations.

```
./igir.exe link \
--symlink \
--symlink-relative \
--dat Datfiles/No-Intro\ Love\ Pack\ \(Standard\)\ \(2025-02-24\)/No-Intro/Nintendo\ -\ Nintendo\ 64\ \(BigEndian\)\ \(20250208-050759\).dat \
--input ROMs/Bank/Nintendo\ -\ Nintendo\ 64\ \(BigEndian\) \
--output ROMs/1G1R \
--dir-dat-name \
--single \
--prefer-parent
```
```
<game name="1080 Snowboarding (Europe) (En,Ja,Fr,De)" id="0006">
	<description>1080 Snowboarding (Europe) (En,Ja,Fr,De)</description>
	<rom name="1080 Snowboarding (Europe) (En,Ja,Fr,De).z64" size="16777216" crc="75a21679" md5="632c98cf281cda776e66685b278a4fa6" sha1="637d92b08dbfe7c2f9d5e338835b1fce5f4a87d0" sha256="a5d47b9b21bc2c234a0e5c8a1f7eb0e893a914e17a0755318b48c5ad15b7d13c" status="verified" serial="NTEP"/>
</game>
<game name="1080 Snowboarding (Japan, USA) (En,Ja)" id="0007" cloneofid="0006">
	<description>1080 Snowboarding (Japan, USA) (En,Ja)</description>
	<rom name="1080 Snowboarding (Japan, USA) (En,Ja).z64" size="16777216" crc="08fe81c7" md5="fa27089c425dbab99f19245c5c997613" sha1="79cd1166c365e5809dec9b62e6d40d6032d5db3a" sha256="5e9d7168e5786ba1bd4b643431ba7100ff3d7a09e558acae15438d426c0f34df" status="verified" serial="NTEA"/>
</game>
<game name="1080 Snowboarding (USA) (En,Ja) (LodgeNet)" id="1136" cloneofid="0006">
	<category>Games</category>
	<description>1080 Snowboarding (USA) (En,Ja) (LodgeNet)</description>
	<rom name="1080 Snowboarding (USA) (En,Ja) (LodgeNet).z64" size="16777216" crc="67e010d2" md5="c6061ad1b4446c4db57cdf094da7c534" sha1="7266eef53af8f2c21f3e3288258121f97eddfa7e"/>
</game>
```

Outputs :
- 1080 Snowboarding (Europe) (En,Ja,Fr,De)
- 1080 Snowboarding (USA) (En,Ja) (LodgeNet)

_Originally posted by @R1nlz3r in https://github.com/emmercm/igir/discussions/1484_
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `7c523dbbc26ae505274c7d8a83074e288ae70c0f`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `main`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "emmercm_igir__1486__7c523db",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
