# Locate the commit that introduced this regression

A regression was reported against `dotnet/runtime`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
Linux build: The dependency target "inject_debug_resources_coreclr" of target "runtimeinfo" does not exist.   

Sometime recently, I've become unable to build dotnet/runtime on Linux Ubuntu 20.04.2 LTS.

Steps:

1. 
2. `git clean -xdf` (just for good measure)
3. `./build.sh -s clr+libs -rc release`

Result:

<pre>
  -- Configuring done
  CMake Error at debug/runtimeinfo/CMakeLists.txt:34 (add_dependencies):
    The dependency target "inject_debug_resources_coreclr" of target
    "runtimeinfo" does not exist.
  
  
  -- Generating done
  CMake Generate step failed.  Build files cannot be regenerated correctly.
  /code/personal/dotnet/runtime/src/coreclr
</pre>

I don't think anything in particular changed in my environment, and nor do I see any other error higher up in the build logs. I tried a branch that is a few weeks old and was able to build it successfully.

Any assistance getting the build working again would be appreciated. 

I did a git bisect and it seems that the following commit is what broke it for me:
```

## What you have

- `/testbed/repo` is a git clone of `dotnet/runtime` truncated just after the regression was
  reported.  `HEAD` is `b80ddefa8db351f4ed697a686d8b6ba1dd927c52` and the full history behind it is present.
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
