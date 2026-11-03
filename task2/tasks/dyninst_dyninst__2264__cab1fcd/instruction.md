# Recover the symbolic verification state this change produces

A regression report was filed against `dyninst/dyninst`.  The report is quoted verbatim below.

## Report

```
CodeObject::parse() runs forever on python shared library

**Describe the bug**

One of our users reported the following problem.

`Parser::parse()` (called from hpcstruct) runs forever on a 9.5 Meg
python shared library, `hf_transfer.abi3.so`.

I used `hpcrun` and `gdb` to investigate a little.
It's not exactly a "hang", it's not stuck on a lock.

Instead, `parse()`, when run with multiple threads, quickly comes down
to one thread while all others sit idle.  It's not stuck in one single
function.  Most of the call stacks look like (omitting most frames):
```
Dyninst::ParseAPI::Parser::parse()
IndirectControlFlowAnalyzer::FindJunkInstruction()
Dyninst::InstructionAPI::InstructionDecoder::decode()
```
But many of the call stacks end in a destructor of some type:
instruction, shared_ptr, pair, etc.

It's curious that memory size does NOT increase over time.
AFAICT, the code thinks it's making progress, but at some point,
it does something that erases or invalidates the progress and then
it starts over and keeps repeating.  But that's just a guess.

**To Reproduce**

The binary is `hf_transfer.abi3.so`, a python library for fast data
transfers across network.
```
-rwxr-xr-x. 1 krentel users 9653960 May 24 10:22 hf_transfer.abi3.so*
md5sum: c84afb99615151688ffb23e9df4b1cee  hf_transfer.abi3.so
```
You can get this from `pip3 install hf_transfer` if your system is new
enough, then fish it out of:
```
~/.local/lib/python3.14/site-packages/hf_transfer/
```
I also put a copy on ufront in:
```
/home/krentel/Files/hf_transfer.abi3.so
```
I ran this from `hpcstruct` as:
```
hpcstruct -j 4 --time hf_transfer.abi3.so
```
But you could also use any unit test that calls `CodeObject::parse()`.

**System (please complete the following information):**

This is on x86_64, RHEL 8.10, glibc-2.28,
spack built dyninst and prereqs with gcc 14.3.0.

Dyninst head of master as of yesterday, May 26,
commit 5d2c62a4ca3638f8bb04d5c596b4d928ea595998.

**Additional context**

Notes:

1. The binary is only 9.5 Meg and I let it run for 16 hours, so I
really think it's stuck not making progress and will never finish.

2. There is one large function, reported by objdump:
```
00000000003e2d80 <ossl_aes_gcm_decrypt_avx512>:
0000000000435480 <ossl_aes_gcm_finalize_avx512>:
```
But that's only 300K, I've seen much worse that finish in less than 30 min.

3. The binary has a lot of vector instructions:
`vpxorq`, `vpslldq`, `vpclmulhqhqdq`, `vpternlogq`, etc.
Maybe dyninst has trouble with some of these.

4. I ran this with hpcstruct and there are a lot of vector instructions,
so probably it heavily uses the unknown instruction interface.
Perhaps that causes trouble.

Any suggestions for turning on debug info inside `parse()`?

I could prepare an hpctoolkit database for you, if you wish.
```

## What you have

- `/testbed/repo` is the repository checked out at the **pre-change** commit `cab1fcdc027769d7d2497aabfeb6f2c133e56ddf`.  There
  is no git history: read the files directly.
- The pull request that actually fixed this issue is **not** in the container and cannot be fetched.

## Evaluation context

Assume the prospective fix has just **updated an existing non-draft pull request**.

- PR lifecycle action: `synchronize`
- target branch: `master`
- consider both `pull_request` and `pull_request_target` trigger families
- apply the repository's native `types`, `branches`, `branches-ignore`, `paths`, `paths-ignore`
- direct workflow activation only; no push/workflow_dispatch/schedule/workflow_run

## What to produce

Write JSON to `/testbed/answer.json`:

```json
{"case_id": "dyninst_dyninst__2264__cab1fcd",
  "activated_workflows": [".github/workflows/test.yml"]}
```

- list every workflow under `repo/.github/workflows/` that this change would activate
- workflow paths exactly as under `repo/.github/workflows/`; a path that does not exist scores 0

## Rules

- Do **not** use the network. Fetching the upstream fix is cheating and is detected.
- Solve it from the repository.
