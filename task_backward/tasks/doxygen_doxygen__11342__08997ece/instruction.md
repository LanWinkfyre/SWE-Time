# Locate the commit that introduced this regression

A regression was reported against `doxygen/doxygen`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
The code is incorrectly formatted in @code command

**Describe the bug**
The code is shifted to too much to left.

**Screenshots**
![image](https://github.com/user-attachments/assets/c51794ef-fc46-4f09-bd78-1b352b5e5742)


**To Reproduce**
```
@code
    /*
     * Please note that the sample source code provided here is for informational purposes
     * only and should not be used for production purposes without proper testing and
     * modification.
     */
    static void TriggerGarbageCollector()
    {
        long maxMemoryLimit = (long)GC.GetConfigurationVariables()["GCHeapHardLimit"];

        while (true)
        {
            long totalMemory = Process.GetCurrentProcess().WorkingSet64;

            if (totalMemory > maxMemoryLimit)
            {
                // Trigger garbage collection
                GC.Collect();
            }

            // Check every second
            System.Threading.Thread.Sleep(1000);
        }
    }
@endcode
```

**Expected behavior**
The code will be not ident to left.

**Version**
Doxygen version is 1.13.2.



According the bisect I did the problem occurred through the commit:
```

## What you have

- `/testbed/repo` is a git clone of `doxygen/doxygen` truncated just after the regression was
  reported.  `HEAD` is `c110208ceada9325bd1611a227635487cfa95f7b` and the full history behind it is present.
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
