# Locate the commit that introduced this regression

A regression was reported against `cue-lang/cue`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Runtime error: invalid memory adress

<!--
Please answer these questions before submitting your issue. Thanks!
To ask questions, see https://github.com/cue-lang/cue#contact.
-->

### What version of CUE are you using (`cue version`)?

<pre>
$ cue version
cue version v0.16.1

CUE language version v0.16.1
</pre>

### Does this issue reproduce with the latest stable release?

v0.16.1 _is_ the latest stable release. So, yes.


### What did you do?

I created this file, `problem.cue`:

```cue

#v1: {
        version: "2025-09"
        mystery: #Problem.uuid
}

#v2: { version: "2025-10" }

#v3: { version: "2025-11" }

#Problem: {
    #v1 | #v2 | #v3

	uuid!: string

	license: *"unknown" | "public domain" 
	if license != "public domain" { }
}
```

and this file, `mini.yaml`:

```yaml
uuid: 550e8400-e29b-41d4-a716-446655440000
problem_format_version: 2025-09
```

and then ran

```
> cue vet mini.yaml problem.cue -d "#Problem"
panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x2 addr=0x160 pc=0x104cdba0c]
```

### What did you expect to see?

An error message (if the YAML does not validate or the CUE is invalid) or nothing (if the YAML validates)

### What did you see instead?

`panic: runtime error: invalid memory address or nil pointer dereference`

I can copy-paste the CUE into the cue playground and that just hangs the web interface.



It might be a good idea to backport a revert to v0.16.2 in any case.
```

## What you have

- `/testbed/repo` is a git clone of `cue-lang/cue` truncated just after the regression was
  reported.  `HEAD` is `35cefbf9b4880261ad6dcdecce7c7e44a79a313c` and the full history behind it is present.
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
